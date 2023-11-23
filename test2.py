def get_determinant(matrix):
    '''Function that gets the deteriminant of a matrix'''
    print(matrix)
    if len(matrix) == 2:
        # Base case
        # |a b|
        # |c d|
        # det = (a * d) - (b * c)
        return matrix[0][0] * matrix [1][1] - matrix[0][1] * matrix[1][0]
    
    # Creates a matrix with the size of n-1*n-1
    # where n = amount of rows in original matrix
    smallerMatrix = []
    for row in range(1,len(matrix)):
        smallerMatrix.append(matrix[row][1:])

    determinant = 0
    for column in range(len(matrix)):
        if column % 2 == 0:
            # Adds the product of the current element on the first line with
            # the determinant of the smaller matrix.
            determinant += matrix[0][column] * get_determinant(smallerMatrix)
        else:
            # Same as above but subtracts.
            determinant -= matrix[0][column] * get_determinant(smallerMatrix)
        
        # All submatrixes has been calculated. Therefore returning the determinant.
        if column == len(matrix) - 1:
            return determinant
        
        # Updates smallerMatrix for the next iteration. 
        for row in range(len(smallerMatrix)):
            smallerMatrix[row][column] = matrix[row+1][column]

if __name__ == '__main__':
    myMatrix = [
            [3, 5, 5, 1, 3],
            [3, 5, 1, 1, 4],
            [5, 0, 6, 1, 3],
            [4, 5, 7, 6, 5],
            [2, 4, 5, 6, 2]
        ]
    myMatrix_2 = [
            [1,1,1,6],
            [5,1,6,7],
            [2,5,0,7],
            [3,3,5,4]
        ]

    print(get_determinant(myMatrix))  # 0
    # print(get_determinant(myMatrix_2))
