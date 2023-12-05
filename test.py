import random, copy, time, numpy as np

start = time.time()


def determinant(matrix):
	# print(matrix)
	d = 0
	if len(matrix[0]) == 2:
     
     	# |a1 a2|
        # |a3 a4|
        # determinant = (a * a4) - (a2 * a3)
		return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
	else:
		for index in range(len(matrix)):
			if index % 2 == 0:
				d += matrix[index][0] * determinant([row[1:] for row in matrix if matrix.index(row) != index])
			else:
				d -= matrix[index][0] * determinant([row[1:] for row in matrix if matrix.index(row) != index])
		return d   
    
    
    
rows = int(input("Rows: "))
collumns = int(input("Collumns: "))

myMatrix = []
for i in range(rows):
    
    temp_list = [random.randint(1, 10) for num in range(collumns)]
    myMatrix.append(copy.deepcopy(temp_list))
    
det = np.linalg.det(myMatrix) 
  
print(round(det)) 

print(determinant(myMatrix))
end = time.time()
time_elapsed = end - start


if time_elapsed < 60:
    print(f"{round(time_elapsed, 2)} s")

if time_elapsed > 60:
    seconds = round(time_elapsed % 60, 2)
    minutes = (time_elapsed - seconds)/60
    print(f"{minutes} m {seconds} s")