#include <iostream>
#include <fstream>
#include <string>
#include "logic.h"

using std::cout, std::endl, std::ifstream, std::string, std::stringstream;

/** //GOOD
 * TODO: Student implement this function
 * Load representation of the dungeon level from file into the 2D map.
 * Calls createMap to allocate the 2D array.
 * @param   fileName    File name of dungeon level.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @param   player      Player object by reference to set starting position.
 * @return  pointer to 2D dynamic array representation of dungeon map with player's location., or nullptr if loading fails for any reason
 * @updates  maxRow, maxCol, player
 */
char** loadLevel(const string& fileName, int& maxRow, int& maxCol, Player& player) {

    ifstream myfile (fileName);
    if (!myfile.is_open()) {
        return nullptr;
    }
    myfile >> maxRow >> maxCol; //Get dimensions //Test case here where the file has 2_ _2 (two spaces)
    if (myfile.fail()) {
        return nullptr;
    }
    if ((maxRow > 999999) || (maxCol > 999999)) {
        return nullptr;
    }
    if ((maxRow <= 0) || (maxCol <= 0)) {
        return nullptr;
    }

    myfile >> player.row >> player.col;
    if (myfile.fail()) {
        return nullptr;
    }
    if ((player.row >= maxRow) || (player.col >= maxCol)) { //Player cant be outside map 
        return nullptr;
    }
    if ((player.row < 0) || (player.col < 0)) { //Make sure players on the map
        return nullptr;
    }

    // Allocate memory for a 2D map
    char** map = createMap(maxRow, maxCol);
    if (map == nullptr) {
        return nullptr;
    }
    bool playerescape = false; //When player leaves

    for (int i = 0; i < maxRow; i++) {
        for (int j = 0; j < maxCol; j++) {

            myfile >> map[i][j];
            //What if theres not enough characters
            if (myfile.fail()) {
                deleteMap(map, maxRow);
                return nullptr;
            }
            //Make sure all inputs are valid
            if ((map[i][j] != TILE_AMULET) && (map[i][j] != TILE_MONSTER) && (map[i][j] != TILE_OPEN) && (map[i][j] != TILE_PILLAR) && 
            (map[i][j] != TILE_PLAYER) && (map[i][j] != TILE_TREASURE) && (map[i][j] != TILE_DOOR) && (map[i][j] != TILE_EXIT)) {
                deleteMap(map, maxRow);
                return nullptr;
            }
            if ((map[i][j] == TILE_DOOR) || (map[i][j] == TILE_EXIT)) {
                playerescape = true;
            }
        }
    }
    if (playerescape == false) {
        deleteMap(map, maxRow);
        return nullptr;
    }
    //From loading seam carving, make sure theres not too many values
    string extra;
    myfile >> extra;
    if (extra != "") {
        deleteMap(map, maxRow);
        return nullptr;
    }
    map[player.row][player.col] = TILE_PLAYER;

    return map;
}

/** //GOOD
 * TODO: Student implement this function
 * Translate the character direction input by the user into row or column change.
 * That is, updates the nextRow or nextCol according to the player's movement direction.
 * @param   input       Character input by the user which translates to a direction.
 * @param   nextRow     Player's next row on the dungeon map (up/down).
 * @param   nextCol     Player's next column on dungeon map (left/right).
 * @updates  nextRow, nextCol
 */
void getDirection(char input, int& nextRow, int& nextCol) {

    switch (input) {
        case MOVE_UP:
            nextRow -= 1;
            break;
        case MOVE_LEFT:
            nextCol -= 1;
            break;
        case MOVE_RIGHT:
            nextCol += 1;
            break;
        case MOVE_DOWN:
            nextRow += 1;
            break;
    }
}

/** //GOOD
 * TODO: [suggested] Student implement this function
 * Allocate the 2D map array.
 * Initialize each cell to TILE_OPEN.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @return  2D map array for the dungeon level, holds char type.
 */
char** createMap(int maxRow, int maxCol) {

    if ((maxRow <= 0) || (maxCol <= 0)) {
        return nullptr;
    }
    // create a 2D array
    char** map = new char*[maxRow];

    for (int i = 0; i < maxRow; i++) {//Access maxRow
        map[i] = new char[maxCol];
    }

    for (int i = 0; i < maxRow; i++) {
        for (int j = 0; j < maxCol; j++) {
            map[i][j] = TILE_OPEN; //Default it to TILE_OPEN
        }
    }
    return map;
}

/** //GOOD
 * TODO: Student implement this function
 * Deallocates the 2D map array.
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @return None
 * @update map, maxRow
 */
void deleteMap(char**& map, int& maxRow) {

    if (map != nullptr) {
        for (int i = 0; i < maxRow; i++) { //First loop through each row to deallocate memory
            delete[] map[i];
        }
        delete[] map; // Deallocate memory for array of pointers
    }
    map = nullptr;
    maxRow = 0;
}

/** //GOOD
 * TODO: Student implement this function
 * Resize the 2D map by doubling both dimensions.
 * Copy the current map contents to the right, diagonal down, and below.
 * Do not duplicate the player, and remember to avoid memory leaks!
 * You can use the STATUS constants defined in logic.h to help!
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height), to be doubled.
 * @param   maxCol      Number of columns in the dungeon table (aka width), to be doubled.
 * @return  pointer to a dynamically-allocated 2D array (map) that has twice as many columns and rows in size.
 * @update maxRow, maxCol
 */
char** resizeMap(char** map, int& maxRow, int& maxCol) {

    int newmaxRow = 2 * maxRow;
    int newmaxCol = 2 * maxCol;

    if (map == nullptr) { //Check that the map is valid
        return nullptr;
    }
    else if ((maxRow <= 0) || (maxCol <= 0)) {
        return nullptr;
    }
    //Make a new big map
    char** bigMap = createMap(newmaxRow, newmaxCol);

    for (int i = 0; i < maxRow; i++) {
        for (int j = 0; j < maxCol; j++) {

            if (map[i][j] == TILE_PLAYER) {
                bigMap[i][j] = TILE_PLAYER;
                bigMap[i + maxRow][j + maxCol] = TILE_OPEN;
                bigMap[i + maxRow][j] = TILE_OPEN;
                bigMap[i][j + maxCol] = TILE_OPEN;
            } else {
                bigMap[i][j] = map[i][j];
                bigMap[i + maxRow][j + maxCol] = map[i][j];
                bigMap[i + maxRow][j] = map[i][j];
                bigMap[i][j + maxCol] = map[i][j];
            }
        }
    }
    //deallocate memory from old map 
    deleteMap(map, maxRow);

    //update dimensions
    maxRow = newmaxRow;
    maxCol = newmaxCol;
    return bigMap;
}

/**
 * TODO: Student implement this function
 * Checks if the player can move in the specified direction and performs the move if so.
 * Cannot move out of bounds or onto TILE_PILLAR or TILE_MONSTER.
 * Cannot move onto TILE_EXIT without at least one treasure. 
 * If TILE_TREASURE, increment treasure by 1.
 * Remember to update the map tile that the player moves onto and return the appropriate status.
 * You can use the STATUS constants defined in logic.h to help!
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @param   player      Player object to by reference to see current location.
 * @param   nextRow     Player's next row on the dungeon map (up/down).
 * @param   nextCol     Player's next column on dungeon map (left/right).
 * @return  Player's movement status after updating player's position.
 * @update map contents, player
 */
int doPlayerMove(char** map, int maxRow, int maxCol, Player& player, int nextRow, int nextCol) {

    if ((nextRow < 0) || (nextRow > (maxRow - 1))) {
        return STATUS_STAY;
    }
    else if ((nextCol < 0) || (nextCol > (maxCol - 1))) {
        return STATUS_STAY;
    }
    else if ((map[nextRow][nextCol] == TILE_PILLAR) || (map[nextRow][nextCol] == TILE_MONSTER)) {
        return STATUS_STAY; //Player got eaten or ran into a wall
    }
    else if (map[nextRow][nextCol] == TILE_TREASURE) { //If player picks up treasure
        map[player.row][player.col] = TILE_OPEN; //position previous is empty
        player.row = nextRow; //update positions
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        player.treasure += 1; //player has got treasure
        return STATUS_TREASURE; //treasures position is the player
    }
    else if ((map[nextRow][nextCol] == TILE_EXIT) && (player.treasure == 0)) {
        return STATUS_STAY;
    }
    else if ((map[nextRow][nextCol] == TILE_EXIT) && (player.treasure > 0)) { //Player can only leave if has treasure and position is exit
        map[player.row][player.col] = TILE_OPEN;
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_ESCAPE;
    }
    else if (map[nextRow][nextCol] == TILE_DOOR) { //leaving room
        map[player.row][player.col] = TILE_OPEN;
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_LEAVE;
    }
    else if (map[nextRow][nextCol] == TILE_AMULET){ //player gets on amulet
        map[player.row][player.col] = TILE_OPEN;
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_AMULET;
    }
    else if (map[nextRow][nextCol] == TILE_OPEN){ //moved to open tile
        map[player.row][player.col] = TILE_OPEN;
        player.row = nextRow;
        player.col = nextCol;
        map[nextRow][nextCol] = TILE_PLAYER;
        return STATUS_MOVE;
    }

    return STATUS_MOVE;
}

/**
 * TODO: Student implement this function
 * Update monster locations:
 * We check up, down, left, right from the current player position.
 * If we see an obstacle, there is no line of sight in that direction, and the monster does not move.
 * If we see a monster before an obstacle, the monster moves one tile toward the player.
 * We should update the map as the monster moves.
 * At the end, we check if a monster has moved onto the player's tile.
 * @param   map         Dungeon map.
 * @param   maxRow      Number of rows in the dungeon table (aka height).
 * @param   maxCol      Number of columns in the dungeon table (aka width).
 * @param   player      Player object by reference for current location.
 * @return  Boolean value indicating player status: true if monster reaches the player, false if not.
 * @update map contents
 */
bool doMonsterAttack(char** map, int maxRow, int maxCol, const Player& player) {

    for (int i = (player.col + 1); i < maxCol; i++) {

        if (map[player.row][i] == TILE_PILLAR) { //Monster cant run into pillar
            break;
        }
        if (map[player.row][i] == TILE_MONSTER) {
            map[player.row][i - 1] = TILE_MONSTER; //Monster moves close to player
            map[player.row][i] = TILE_OPEN; //Old tile is open now
        }
    }
    for (int i = (player.col - 1); i >= 0; i--) {
    
        if (map[player.row][i] == TILE_PILLAR) {
            break;
        }
        if (map[player.row][i] == TILE_MONSTER) {
            map[player.row][i + 1] = TILE_MONSTER;
            map[player.row][i] = TILE_OPEN;
        }
    }
    for (int i = (player.row + 1); i < maxRow; i++) {

        if (map[i][player.col] == TILE_PILLAR) {
            break;
        }
        else if (map[i][player.col] == TILE_MONSTER) {
            map[i - 1][player.col] = TILE_MONSTER;
            map[i][player.col] = TILE_OPEN;
        }
    }
    for (int i = (player.row - 1); i >= 0; i--) { //Monster doesnt move up

        if (map[i][player.col] == TILE_PILLAR) {
            break;
        }
        else if (map[i][player.col] == TILE_MONSTER) {
            map[i + 1][player.col] = TILE_MONSTER;
            map[i][player.col] = TILE_OPEN;
        }
    }
    if (map[player.row][player.col] == TILE_MONSTER) {
        return true;
    }
    return false;
}
