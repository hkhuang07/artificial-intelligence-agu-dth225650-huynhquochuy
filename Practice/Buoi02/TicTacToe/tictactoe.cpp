#include <algorithm>
#include <iostream>
#include <list>
#include <vector>

using namespace std;

enum state { PLAYING, XWIN, OWIN, DRAW };

constexpr const int infinity = 10;

state checkWin(const int (&gameBoard)[9])
{
    for (int i = 0; i != 3; ++i) {
        if (gameBoard[0 + 3 * i] + gameBoard[1 + 3 * i] + gameBoard[2 + 3 * i] == 3) {
            return XWIN;
        } else if (gameBoard[0 + 3 * i] + gameBoard[1 + 3 * i] + gameBoard[2 + 3 * i] == -3) {
            return OWIN;
        }
        if (gameBoard[0 + i] + gameBoard[3 + i] + gameBoard[6 + i] == 3) {
            return XWIN;
        } else if (gameBoard[0 + i] + gameBoard[3 + i] + gameBoard[6 + i] == -3) {
            return OWIN;
        }
    }
    if (gameBoard[0] + gameBoard[4] + gameBoard[8] == 3
        || gameBoard[2] + gameBoard[4] + gameBoard[6] == 3) {
        return XWIN;
    }
    if (gameBoard[0] + gameBoard[4] + gameBoard[8] == -3
        || gameBoard[2] + gameBoard[4] + gameBoard[6] == -3) {
        return OWIN;
    }
    if (std::find(gameBoard, gameBoard + 9, 0) != gameBoard + 9) {
        return PLAYING;
    }
    return DRAW;
}

void generate_moves(const int (&gameBoard)[9], list<int> &moves)
{
    for (int i = 0; i < 9; i++) {
        if (gameBoard[i] == 0) {
            moves.push_back(i);
        }
    }
}

int evaluate_position(const int (&gameBoard)[9], int playerTurn)
{
    state currentGameState = checkWin(gameBoard);
    if (currentGameState != PLAYING) {
        if ((playerTurn == 1 && currentGameState == XWIN) || (playerTurn == -1 && currentGameState == OWIN))
            return +infinity;
        else if ((playerTurn == -1 && currentGameState == XWIN) || (playerTurn == 1 && currentGameState == OWIN))
            return -infinity;
        else if (currentGameState == DRAW)
            return 0;
    }
    return -1;
}

int MaxMove(int (&gameBoard)[9], int playerTurn)
{
    int pos_val = evaluate_position(gameBoard, playerTurn);
    if (pos_val != -1) return pos_val;

    int bestScore = -infinity;
    list<int> movesList;
    generate_moves(gameBoard, movesList);

    while (!movesList.empty()) {
        gameBoard[movesList.front()] = playerTurn;
        int score = -MaxMove(gameBoard, -playerTurn);
        if (score > bestScore) {
            bestScore = score;
        }
        gameBoard[movesList.front()] = 0;
        movesList.pop_front();
    }
    return bestScore;
}

int MiniMax(int (&gameBoard)[9], int playerTurn)
{
    int bestScore = -infinity;
    list<int> movesList;
    vector<int> bestMoves;
    generate_moves(gameBoard, movesList);

    while (!movesList.empty()) {
        gameBoard[movesList.front()] = playerTurn;
        int score = -MaxMove(gameBoard, -playerTurn);
        if (score > bestScore) {
            bestScore = score;
            bestMoves.clear();
            bestMoves.push_back(movesList.front());
        } else if (score == bestScore) {
            bestMoves.push_back(movesList.front());
        }
        gameBoard[movesList.front()] = 0;
        movesList.pop_front();
    }

	#if 0
		int index = bestMoves.size();
		if (index > 0) {
			time_t secs;
			time(&secs);
			srand((uint32_t)secs);
			index = rand() % index;
		}
		return bestMoves[index];
	#else
		return bestMoves.front();
	#endif
}

void print(const int (&gameBoard)[9])
{
    const char cs[] = {'O', '.', 'X'};

    std::cout << "--------" << std::endl;
    for (int i = 0; i != 3; ++i) {
        for (int j = 0; j != 3; ++j) {
            std::cout << cs[1 + gameBoard[3 * i + j]];
        }
        std::cout << std::endl;
    }
}

int main()
{
    int gameBoard[9] {};

    int player = 1;
    while (checkWin(gameBoard) == PLAYING) {
        gameBoard[MiniMax(gameBoard, player)] = player;
        print(gameBoard);
        player *= -1;
        getchar();
    }
    return 0;
}
