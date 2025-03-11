import numpy as np

class ReadVaspOutput:
    def __init__(self,directory):
        self.directory = directory
        self.data = {}
        self._parse_file()
    
    def _parse_file(self):
        with open(self.directory+"/"+"OUTCAR", "r") as file:
            lines = file.readlines()
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

        if self.data["soc"] == "F":
            m_z = m_x; m_x = np.zeros((natoms,4)); m_y = np.zeros((natoms,4))
        self.data["magmom"] = np.stack((m_x[:,3],m_y[:,3],m_z[:,3]), axis=1)

    def get(self, key, default=None):
        return self.data.get(key, default)