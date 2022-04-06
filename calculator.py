# Run Anaconda Environment
# streamlit run calculator.py

import streamlit as st
from sympy import Matrix, lcm

def getCoeffs(N, factors, elements):
    "Constructs a matrix and gets the matrix nullspace. the nullspace corresponds to the coefficients of a balanced chem equation."
    
    # construct initial matrix
    eN = len(elements)
    matrix = [[0 for i in range(N)] for j in range(eN)]
    elemIndex = {}
    for i in range(eN):
        elemIndex[elements[i]] = i
    for col, elem, val in factors:
        matrix[elemIndex[elem]][col] = val
    #print(*matrix)

    # use sympy to get nullspace of matrix
    symMatrix = Matrix(matrix)
    coeffs = symMatrix.nullspace()[0]
    #print(*coeffs)

    # convert coefficients to its lowest integer form by using lcm
    multi = lcm([val.q for val in coeffs])
    coeffs = multi*coeffs
    
    return list(coeffs)

def processInput(s):
    "processes inputted chem equation."
    factors = []
    elements = []
    
    Sreactant, Sproduct = s.split("->")
    reactants = Sreactant.split("+")
    products = Sproduct.split("+")

    leftN = len(reactants)
    rightN = len(products)

    for i in range(leftN):
        addend = reactants[i]
        lst = addend.split("*")
        for factor in lst:
            elem, moles = factor.split(":")
            factors.append((i, elem, int(moles)))
            elements.append(elem)
    
    for i in range(rightN):
        addend = products[i]
        lst = addend.split("*")
        for factor in lst:
            elem, moles = factor.split(":")
            factors.append((i+leftN, elem, -int(moles)))
    
    return (leftN, rightN, factors, elements, reactants, products)
    
if __name__ == '__main__':
    #config
    st.set_page_config(
        page_title="Chem Equation Calculator",
    )

    # title
    st.title("Chemical Equation Calculator")
    st.caption("© Bryan Francisco")

    # input
    unbalanced = st.text_input('Insert Chemical Equation:', 'C:4*H:10+O:2->C:1*O:2+H:2*O:1')
    # on button click
    bttn = st.button('Balance equation')

    if bttn:
        # process
        error_code = 0
        try:
            error_code += 1
            leftN, rightN, factors, elements, reactants, products = processInput(unbalanced)
            
            error_code += 1
            coeffs = getCoeffs(leftN + rightN, factors, elements)
            
            error_code += 1
            st.subheader("Balanced Chemical Equation:")
            latex = ""
            
            for i in range(leftN):
                latex += "\\textcolor{blue}{" + str(coeffs[i]) + "} "
                facts = reactants[i].split('*')
                for addend in facts:
                    elem, moles = addend.split(':')
                    latex += elem
                    if moles != '1':
                        latex += '_' + moles
                latex += '+'
            latex = latex[:-1]
            latex += ' \\rightarrow '

            for i in range(rightN):
                latex += "\\textcolor{blue}{" + str(coeffs[i+leftN]) + "} "
                facts = products[i].split('*')
                for addend in facts:
                    elem, moles = addend.split(':')
                    latex += elem
                    if moles != '1':
                        latex += '_' + moles
                latex += '+'
            latex = latex[:-1]
            
            st.latex(latex)
            
            # H:1*Cl:1+Ca:1*C:1*O:3->Ca:1*Cl:2+H:2*O:1+C:1*O:2
            # C:3*H:6+O:2->C:1*O:2+H:2*O:1
            # S:1+H:1*N:1*O:3->H:2*S:1*O:4+N:1*O:2+H:2*O:1
            # C:4*H:10+O:2->C:1*O:2+H:2*O:1
        except:
            st.error("An error occured." + " Exit code:" + str(error_code))