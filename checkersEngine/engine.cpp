#include "AIPlayer.h"
#include "CheckersBoard.h"
#include <iostream>
#include <vector>


using namespace checkers;
static const Piece::PieceType EmptyPieceLayout[CheckersBoard::NumberOfSquares] {};


int main( int argc, char **argv ){
  //std::cout << argc << "\n";
  //if( argc != 65 ){ return 1; }

  if( argc < 2 ){ return 1; }
  int state = 0;

  if( !std::string(argv[1]).compare("AI") ){
    state = 0;
  }else{
    state = 1;
  }


  CheckersBoard board(EmptyPieceLayout, CheckersBoard::SideType::White);

  for( int i = 2; i < argc; i++){
    int c = (i-2)%8;
    int r = (i-2)/8;

    std::cout << r << " " << c << ": " << argv[i][0] << "\n";

    if( argv[i][0] == '1' ){
      board.SetPiece(Pos{c,r}, Piece::PieceType::White);
    }else if( argv[i][0] == '2'){
      board.SetPiece(Pos{c,r}, Piece::PieceType::Black);
    }

  }

  if( state == 0 ){

    AIPlayer aiPlayer;
    Move move = aiPlayer.ChooseBestMove(board);

    if( move.IsAdjacentMove() == true ){
      std::cout <<  "move\n";
    }else{
      std::cout << "kill\n";
    }
    std::cout << move.from.row << " " << move.from.column << "\n";
    std::cout << move.to.row << " " << move.to.column << "\n";

  }

  return 0;
}
