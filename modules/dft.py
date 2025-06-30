import numpy as np

class ReadVaspOutput:
    def __init__(self, file_content):
        # If file_content is a path (for local testing), open it
        if isinstance(file_content, str):
            with open(file_content, "r") as file:
                self.lines = file.readlines()
        # If file_content is a file-like object (from Streamlit), read it
        elif hasattr(file_content, 'read'): # Check if it has a read method
            # Read as text (assuming UTF-8 encoding, adjust if needed)
            self.lines = file_content.read().decode("utf-8").splitlines()
        else:
            raise TypeError("file_content must be a file path or a file-like object.")

        self.data = {}
        self._parse_file()
        self._validate_keys()
    
    def _parse_file(self):
        lines = self.lines
        species = []

        for line in lines:
            if "VRHFIN" in line:
                species.append(line.split("=")[1].split(":")[0].strip())
            
        for i in range(len(lines)):
            if "LSORBIT" in lines[i]:
                self.data["soc"] = list(map(str, lines[i].split()))[2]
            if "ions per type =" in lines[i]:
                nions = [int(x) for x in list(map(str,lines[i].split()))[4:]]
                self.data["nions"] = nions; natoms = sum(nions)
            if "direct lattice vectors" in lines[i]:
                lattice = []
                for j in range(i+1, i+4):
                    lattice.append(list(map(float, lines[j].split()))[:3])
                self.data["lattice"] = np.array(lattice)
            if "position of ions in cartesian coordinates  (Angst):" in lines[i]:
                pos_cart = []
                for j in range(i+1, i+1+natoms):
                    pos_cart.append(list(map(float, lines[j].split()))[:3])
                self.data["pos_cart"] = np.array(pos_cart)
            if "magnetization (x)" in lines[i]:
                m_x = []
                for j in range(i+4,i+4+natoms):
                    m_x.append(list(map(float, lines[j].split()))[1:])
                m_x = np.array(m_x)
            if "magnetization (y)" in lines[i]:
                m_y = []
                for j in range(i+4,i+4+natoms):
                    m_y.append(list(map(float, lines[j].split()))[1:])
                m_y = np.array(m_y)
            if "magnetization (z)" in lines[i]:
                m_z = []
                for j in range(i+4,i+4+natoms):
                    m_z.append(list(map(float, lines[j].split()))[1:])
                m_z = np.array(m_z)

        self.data["species"] = species
        if self.data["soc"] == "F":
            m_z = m_x; m_x = np.zeros((natoms,4)); m_y = np.zeros((natoms,4))
        self.data["magmom"] = np.stack((m_x[:,3],m_y[:,3],m_z[:,3]), axis=1)
    
    def _validate_keys(self):
        required_keys = ["lattice", "pos_cart", "nions", "species", "magmom"]
        missing_keys = [key for key in required_keys if key not in self.data]
        if missing_keys:
            raise ValueError(f"Missing required keys in data: {missing_keys}")

    def get(self, key, default=None):
        return self.data.get(key, default)

# Just for SIESTA: to fetch the element symbol from the atomic number
# as the Specie Labels may vary due to custom pseudopotential name
periodic_table = {
    1:  "H",    2:  "He",   3:  "Li",   4:  "Be",   5:  "B",    6:  "C",
    7:  "N",    8:  "O",    9:  "F",    10: "Ne",  11: "Na",  12: "Mg",
    13: "Al",   14: "Si",   15: "P",    16: "S",   17: "Cl",  18: "Ar",
    19: "K",    20: "Ca",   21: "Sc",   22: "Ti",  23: "V",   24: "Cr",
    25: "Mn",   26: "Fe",   27: "Co",   28: "Ni",  29: "Cu",  30: "Zn",
    31: "Ga",   32: "Ge",   33: "As",   34: "Se",  35: "Br",  36: "Kr",
    37: "Rb",   38: "Sr",   39: "Y",    40: "Zr",  41: "Nb",  42: "Mo",
    43: "Tc",   44: "Ru",   45: "Rh",   46: "Pd",  47: "Ag",  48: "Cd",
    49: "In",   50: "Sn",   51: "Sb",   52: "Te",  53: "I",   54: "Xe",
    55: "Cs",   56: "Ba",   57: "La",   58: "Ce",  59: "Pr",  60: "Nd",
    61: "Pm",   62: "Sm",   63: "Eu",   64: "Gd",  65: "Tb",  66: "Dy",
    67: "Ho",   68: "Er",   69: "Tm",   70: "Yb",  71: "Lu",  72: "Hf",
    73: "Ta",   74: "W",    75: "Re",   76: "Os",  77: "Ir",  78: "Pt",
    79: "Au",   80: "Hg",   81: "Tl",   82: "Pb",  83: "Bi",  84: "Po",
    85: "At",   86: "Rn",   87: "Fr",   88: "Ra",  89: "Ac",  90: "Th",
    91: "Pa",   92: "U",    93: "Np",   94: "Pu",  95: "Am",  96: "Cm",
    97: "Bk",   98: "Cf",   99: "Es",  100: "Fm", 101: "Md", 102: "No",
   103: "Lr",  104: "Rf",  105: "Db",  106: "Sg", 107: "Bh", 108: "Hs",
   109: "Mt",  110: "Ds",  111: "Rg",  112: "Cn", 113: "Nh", 114: "Fl",
   115: "Mc",  116: "Lv",  117: "Ts",  118: "Og"
}

class ReadSiestaOutput:
    def __init__(self, file_content):
        # If file_content is a path (for local testing), open it
        if isinstance(file_content, str):
            with open(file_content, "r") as file:
                self.lines = file.readlines()
        # If file_content is a file-like object (from Streamlit), read it
        elif hasattr(file_content, 'read'): # Check if it has a read method
            # Read as text (assuming UTF-8 encoding, adjust if needed)
            self.lines = file_content.read().decode("utf-8").splitlines()
        else:
            raise TypeError("file_content must be a file path or a file-like object.")
        
        self.data = {}
        self._parse_file()
        self._validate_keys()
    
    def _parse_file(self):
        bohr2ang = 0.529177
        lines = self.lines

        for i in range(len(lines)):
            if "siesta: Atomic coordinates (Bohr) and species" in lines[i]:
                pos_cart = []; ion_types = [] ; j = i+1
                while len(lines[j])>1:
                    linesplit = lines[j].split() ; j += 1
                    pos_cart.append(linesplit[1:4]) ; ion_types.append(linesplit[4])
                ion_types = np.array(ion_types) ; pos_cart = np.array(pos_cart) # New
                sorted_indices = np.argsort(ion_types) # New
                ion_types = ion_types[sorted_indices] ; pos_cart = pos_cart[sorted_indices] # New
                elements, nions = np.unique(ion_types, return_counts=True)
                self.data["nions"] = np.array(nions) ; natoms = sum(np.array(nions))
                self.data["pos_cart"] = np.array(pos_cart).astype("float")*bohr2ang
            elif "%block ChemicalSpeciesLabel" in lines[i]:
                species = []
                j = i+1
                while "%endblock ChemicalSpeciesLabel" not in lines[j]:
                    linesplit = lines[j].split() #; species.append(linesplit[2])
                    symbol = periodic_table[int(linesplit[1])] ; species.append(symbol) # New
                    j += 1
                self.data["species"] = species
            elif "outcell: Unit cell vectors (Ang):" in lines[i]:
                lattice = []
                for j in range(i+1, i+4):
                    lattice.append(list(map(float, lines[j].split()))[:3])
                self.data["lattice"] = np.array(lattice)
            elif "Mulliken Atomic Populations:" in lines[i]:
                if len(lines[i+2].split()) == 5:
                    magmom = []
                    for j in range(i+2, i+2+natoms):
                        linesplit = lines[j].split() ; magmom.append([0, 0, linesplit[3]])
                elif len(lines[i+2].split()) == 8:
                    magmom = []
                    for j in range(i+2, i+2+natoms):
                        linesplit = lines[j].split() ; magmom.append(linesplit[4:7])
                else:
                    print("ERROR: Incorret number of spin components !")
                magmom = np.array(magmom)[sorted_indices] # New
                self.data["magmom"] = np.array(magmom).astype("float")

    def _validate_keys(self):
        required_keys = ["lattice", "pos_cart", "nions", "species", "magmom"]
        missing_keys = [key for key in required_keys if key not in self.data]
        if missing_keys:
            raise ValueError(f"Missing required keys in data: {missing_keys}")
    
    def get(self, key, default=None):
        return self.data.get(key, default)

