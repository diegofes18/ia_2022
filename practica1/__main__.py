from practica1 import agent, joc


def main():
    rana = agent.Rana("Miquel")
    #rana2 =agent.Rana('Diego')
    lab = joc.Laberint([rana], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
