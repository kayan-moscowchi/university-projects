import random

def game_printer(twoD_list):
        printer = 0
        print(" ")
        while printer < len(twoD_list):
            print(twoD_list[printer])
            printer += 1

def start():
    scr_flag = False
    scc_flag = False
    mine_flag = False
    height_flag = False
    width_flag = False
    game_matrix = [[]]

    print("\nHello there friend, welcome to python minesweeper game :) ")
    
    height = int(input("\nInsert the number of cells in the height of the box (It must be higher than 3 and lower than 50): "))
    
    while height_flag == False:
        if height < 3 or height > 50:
            height = int(input("\nThe number must be higher than 3 and lower than 50"))
        else:
            height_flag = True

    width = int(input("\nInsert the number of cells in width of the box (It must be higher than 3 and lower than 50): "))

    while width_flag == False:
        if width < 3 or width > 50:
            width = int(input("\nThe number must be higher than 3 and lower than 50"))
        else:
            width_flag = True
    
    mine_count = int(input("\nInsert the number of the mines you want to be in the game (They cannot be more than half of totall number of cells) : "))

    while mine_flag == False:
        if mine_count < height * width / 2:
            mine_flag = True
        elif mine_count == 0:
            mine_count = int(input("\nYou cannot have 0 mines in MINE SWEEPER GAME !?!? : "))        
        else:
            mine_count = int(input("\nNumber of mines cannot be more than half of totall number of cells : "))

    for column in range(width + 1):
        if column < 10:
            game_matrix[0].append("0" + str(column))
        else:
            game_matrix[0].append(str(column))

    for row in range(height):
        if row < 9:
            game_matrix.append(["0" + str(row + 1)])
        else:
            game_matrix.append([str(row + 1)])
        maker = 0
        while maker < (width):
                game_matrix[row + 1].append("xx")
                maker += 1
    
    game_printer(game_matrix)

    while scr_flag == False:
        scr = int(input("\nSpecify the row number of the cell you want to start with : "))
        if scr >= 1 and scr <= height:
            scr_flag = True
        else:
            print("\n*** The row number should be between 1 and " + str(height))
    
    while scc_flag == False:
        scc = int(input("\nSpecify the column number of the cell you want to start with : "))
        if scc >= 1 and scc <= width:
            scc_flag = True
        else:
            print("\n*** The row number should be between 1 and " + str(width))
    
    game_generator(game_matrix, [scr, scc], mine_count)


def game_generator(game_matrix, start_cord, mine_count):
    mine_list = []
    mine_counter = 0

    #bottom left edge
    if start_cord[0] == len(game_matrix) and start_cord[1] == len(game_matrix[0]):
        #top left cell and top midlle and left side
        mine_ban_list = [[(start_cord[0] - 1), (start_cord[1] - 1)], [(start_cord[0] - 1), start_cord[1]], [start_cord[0], (start_cord[1] - 1)]]

    #last row    
    elif start_cord[0] == len(game_matrix):
        #all tops and right and left side
        mine_ban_list = [[(start_cord[0] - 1), (start_cord[1] - 1)], [(start_cord[0] - 1), start_cord[1]], [(start_cord[0] - 1), (start_cord[1] + 1)], [start_cord[0], (start_cord[1] - 1)], [start_cord[0], (start_cord[1] + 1)]]
    
    #last column 
    elif start_cord[1] == len(game_matrix[0]):
        #top left cell and top middle cell and left side and bottom left edge and bottom middle 
        mine_ban_list = [[(start_cord[0] - 1), (start_cord[1] - 1)], [(start_cord[0] - 1), start_cord[1]], [start_cord[0], (start_cord[1] - 1)], [(start_cord[0] + 1), (start_cord[1] - 1)], [(start_cord[0] + 1), start_cord[1]]]
    
    #all normal cells
    else:
        #all 8 cells around the selected cell
        mine_ban_list = [[(start_cord[0] - 1), (start_cord[1] - 1)], [(start_cord[0] - 1), start_cord[1]], [(start_cord[0] - 1), (start_cord[1] + 1)], [start_cord[0], (start_cord[1] - 1)], [start_cord[0], (start_cord[1] + 1)], [(start_cord[0] + 1), (start_cord[1] - 1)], [(start_cord[0] + 1), start_cord[1]], [(start_cord[0] + 1), (start_cord[1] + 1)]]

    mine_ban_list.append([start_cord[0], start_cord[1]])
    
    while mine_counter < mine_count:
        mine_row = random.randrange(1, (len(game_matrix)))
        mine_column = random.randrange(1, (len(game_matrix[0])))
        mine_cord = [mine_row, mine_column]

        if mine_cord not in mine_list and mine_cord not in mine_ban_list:
            mine_list.append(mine_cord)
            mine_counter += 1

    game_matrix = game_runner(game_matrix, [start_cord[0], start_cord[1]], mine_list)
    game_printer(game_matrix)
    player(mine_list, game_matrix)


def player(mine_list, game_matrix):
    row_flag = False
    column_flag = False
    operation_flag = False
    selected_cell = False
    win_checker = 0
    win_flag = True

    while win_checker < len(mine_list) and win_flag == True:
        if game_matrix[mine_list[win_checker][0]][mine_list[win_checker][1]] != "ff":
            win_flag = False
        win_checker += 1
    
    if win_flag == True:
        return("Congrats !\nYOU WON THE GAME !")

    while selected_cell == False:

        while row_flag == False:

            selected_row = int(input("\nSelect a cell row to do operation on it :"))

            if selected_row >= 1 and selected_row <= len(game_matrix):
                row_flag = True
            else:
                print("\n*** You must enter a number between 1 and " + str(len(game_matrix)))
        
        while column_flag == False:
            
            selected_column = int(input("\nSelect a cell column to do operation on it :"))

            if selected_column >= 1 and selected_column <= len(game_matrix[0]):
                column_flag = True
            else:
                print("\n*** You must enter a number between 1 and " + str(len(game_matrix[0])))
        
        if game_matrix[selected_row][selected_column] == "xx" or game_matrix[selected_row][selected_column] == "ff":
            selected_cell = True
        else:
            print("\nYou cannot select this cell.Try another cell")
            row_flag = False
            column_flag = False
        
    while operation_flag == False:
        operation = input("\nselect what operation you want to do ? (click / flag) ")

        if operation == "click":
            if [selected_row, selected_column] in mine_list:
                print("\nThe selected cell was a mine. You LOST !!!")
            else:
                game_matrix = game_runner(game_matrix, [selected_row, selected_column], mine_list)
                game_printer(game_matrix)
                operation_flag = True

        elif operation == "flag":
                game_matrix[selected_row][selected_column] = "ff"
                game_printer(game_matrix)
                operation_flag = True
        else:
            print("\nplease enter a valid operation. select one ---> click / flag")

    player(mine_list, game_matrix)
        
def game_runner(game_matrix, selected_cord, mine_list):
    mine_count = neighbor_mine_counter(game_matrix, [selected_cord[0], selected_cord[1]], mine_list)

    if mine_count == 0:
        game_matrix[selected_cord[0]][selected_cord[1]] = "00"
        #top left cell
        if selected_cord[0] != 1 and selected_cord[1] != 1:
            if game_matrix[(selected_cord[0] - 1)][(selected_cord[1] - 1)] != "00":
                mine_count_tl = neighbor_mine_counter(game_matrix, [(selected_cord[0] - 1), (selected_cord[1] - 1)], mine_list)
                if mine_count_tl != 0:
                    game_matrix[(selected_cord[0] - 1)][(selected_cord[1] - 1)] = "0" + str(mine_count_tl)
                else:
                    game_matrix[(selected_cord[0] - 1)][(selected_cord[1] - 1)] = "00"
                    game_matrix = game_runner(game_matrix, [(selected_cord[0] - 1), (selected_cord[1] - 1)], mine_list)

        #top middle cell
        if selected_cord[0] != 1:
            if game_matrix[(selected_cord[0] - 1)][selected_cord[1]] != "00":
                mine_count_tm = neighbor_mine_counter(game_matrix, [(selected_cord[0] - 1), selected_cord[1]], mine_list)
                if mine_count_tm != 0:
                    game_matrix[(selected_cord[0] - 1)][selected_cord[1]] = "0" + str(mine_count_tm)
                else:
                    game_matrix[(selected_cord[0] - 1)][selected_cord[1]] = "00"
                    game_matrix = game_runner(game_matrix, [(selected_cord[0] - 1), selected_cord[1]], mine_list)

        #top right cell
        if selected_cord[0] != 1 and selected_cord[1] != (len(game_matrix[0]) - 1):
            if game_matrix[(selected_cord[0] - 1)][(selected_cord[1] + 1)] != "00":
                mine_count_tr = neighbor_mine_counter(game_matrix, [(selected_cord[0] - 1), (selected_cord[1] + 1)], mine_list)
                if mine_count_tr != 0:
                    game_matrix[(selected_cord[0] - 1)][(selected_cord[1] + 1)] = "0" + str(mine_count_tr)
                else:
                    game_matrix[(selected_cord[0] - 1)][(selected_cord[1] + 1)] = "00"
                    game_matrix = game_runner(game_matrix, [(selected_cord[0] - 1), (selected_cord[1] + 1)], mine_list)

        #left side cell
        if selected_cord[1] != 1:
            if game_matrix[selected_cord[0]][(selected_cord[1] - 1)] != "00":
                mine_count_ls = neighbor_mine_counter(game_matrix, [selected_cord[0], (selected_cord[1] - 1)], mine_list)
                if mine_count_ls != 0:
                    game_matrix[selected_cord[0]][(selected_cord[1] - 1)] = "0" + str(mine_count_ls)
                else:
                    game_matrix[selected_cord[0]][(selected_cord[1] - 1)] = "00"
                    game_matrix = game_runner(game_matrix, [selected_cord[0], (selected_cord[1] - 1)], mine_list)

        #right side cell
        if selected_cord[1] != (len(game_matrix[0]) - 1):
            if game_matrix[selected_cord[0]][(selected_cord[1] + 1)] != "00":
                mine_count_rs = neighbor_mine_counter(game_matrix, [selected_cord[0], (selected_cord[1] + 1)], mine_list)
                if mine_count_rs != 0:
                    game_matrix[selected_cord[0]][(selected_cord[1] + 1)] = "0" + str(mine_count_rs)
                else:
                    game_matrix[selected_cord[0]][(selected_cord[1] + 1)] = "00"
                    game_matrix = game_runner(game_matrix, [selected_cord[0], (selected_cord[1] + 1)], mine_list)

        #bottom left cell
        if selected_cord[0] != (len(game_matrix) - 1) and selected_cord[1] != 1:
            if game_matrix[(selected_cord[0] + 1)][(selected_cord[1] - 1)] != "00":
                mine_count_bl = neighbor_mine_counter(game_matrix, [(selected_cord[0] + 1), (selected_cord[1] - 1)], mine_list)
                if mine_count_bl != 0:
                    game_matrix[(selected_cord[0] + 1)][(selected_cord[1] - 1)] = "0" + str(mine_count_bl)
                else:
                    game_matrix[(selected_cord[0] + 1)][(selected_cord[1] - 1)] = "00"
                    game_matrix = game_runner(game_matrix, [(selected_cord[0] + 1), (selected_cord[1] - 1)], mine_list)

        #bottom middle cell
        if selected_cord[0] != (len(game_matrix) - 1):
            if game_matrix[(selected_cord[0] + 1)][selected_cord[1]] != "00":
                mine_count_bm = neighbor_mine_counter(game_matrix, [(selected_cord[0] + 1), selected_cord[1]], mine_list)
                if mine_count_bm != 0:
                    game_matrix[(selected_cord[0] + 1)][selected_cord[1]] = "0" + str(mine_count_bm)
                else:
                    game_matrix[(selected_cord[0] + 1)][selected_cord[1]] = "00"
                    game_matrix = game_runner(game_matrix, [(selected_cord[0] + 1), selected_cord[1]], mine_list)

        #bottom right cell
        if selected_cord[0] != (len(game_matrix) - 1) and selected_cord[1] != (len(game_matrix[0]) - 1):
            if game_matrix[(selected_cord[0] + 1)][(selected_cord[1] + 1)] != "00":
                mine_count_br = neighbor_mine_counter(game_matrix, [(selected_cord[0] + 1), (selected_cord[1] + 1)], mine_list)
                if mine_count_br != 0:
                    game_matrix[(selected_cord[0] + 1)][(selected_cord[1] + 1)] = "0" + str(mine_count_br)
                else:
                    game_matrix[(selected_cord[0] + 1)][(selected_cord[1] + 1)] = "00"
                    game_matrix = game_runner(game_matrix, [(selected_cord[0] + 1), (selected_cord[1] + 1)], mine_list)

    else:
        game_matrix[selected_cord[0]][selected_cord[1]] = "0" + str(mine_count)

    return game_matrix

def neighbor_mine_counter(game_matrix, selected_cord, mine_list):
    mines_around = 0

    #top left cell
    if selected_cord[0] != 1 and selected_cord[1] != 1:
        if [(selected_cord[0] - 1) , (selected_cord[1] - 1)] in mine_list:
            mines_around += 1

    #top middle cell
    if selected_cord[0] != 1:
        if [(selected_cord[0] - 1) , selected_cord[1]] in mine_list:
            mines_around += 1

    #top right cell
    if selected_cord[0] != 1 and selected_cord[1] != (len(game_matrix[0]) - 1):
        if [(selected_cord[0] - 1) , (selected_cord[1] + 1)] in mine_list:
            mines_around += 1

    #left side cell
    if selected_cord[1] != 1:
        if [selected_cord[0] , (selected_cord[1] - 1)] in mine_list:
            mines_around += 1

    #right side cell
    if selected_cord[1] != (len(game_matrix[0]) - 1):
        if [selected_cord[0] , (selected_cord[1] + 1)] in mine_list:
            mines_around += 1

    #bottom left cell
    if selected_cord[0] != (len(game_matrix) - 1) and selected_cord[1] != 1:    
        if [(selected_cord[0] + 1) , (selected_cord[1] - 1)] in mine_list:
            mines_around += 1

    #bottom middle cell
    if selected_cord[0] != (len(game_matrix) - 1):
        if [(selected_cord[0] + 1) , selected_cord[1]] in mine_list:
            mines_around += 1

    #bottom right cell
    if selected_cord[0] != (len(game_matrix) - 1) and selected_cord[1] != (len(game_matrix[0]) - 1):
        if [(selected_cord[0] + 1) , (selected_cord[1] + 1)] in mine_list:
            mines_around += 1

    return mines_around

start()