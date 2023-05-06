#include <iostream>

using namespace std;

int main() {
    //noticeGameStart
    cout << "Game start, pleace input a char ^o^";

    //charList
    char charList[] ={'a','b','c','d','e','f','g','h','i','j','k'};

    //random guessTarget
    int randomNum=5; //for test

    char guessTarget = charList[randomNum];

    //gamer input answer
    char gamerInputChar;
    cin >> gamerInputChar;

    int checkFlag = 0;

    //game end util gamer guess true answer
    while(checkFlag==0){
    cout << "Wrong, please guess again:";
    cin >> gamerInputChar;

    //check answer and print msg to gamer
    if(gamerInputChar==guessTarget){
    checkFlag=1;
    }else{
    checkFlag=0;
    }
    }


    while(checkFlag==1){
            cout << "Bingo!";
    //ask gamer 'Do you want to play again\'w\'?\'
            cout << "Do you want to play again\'w\'?(Y or N)";
            char gamerDesire;
            cin >> gamerDesire;
            switch(gamerDesire){
                case 'Y':
                            main(); //遞迴大丈夫？？
                            break;
                case 'N':
                            exit(0);
                            break;
            }
    }

    return 0;
}