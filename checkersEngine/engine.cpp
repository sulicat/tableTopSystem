#include "AIPlayer.h"
#include "CheckersBoard.h"
#include <iostream>
#include <vector>


using namespace checkers;
static const Piece::PieceType EmptyPieceLayout[CheckersBoard::NumberOfSquares] {};


int main( int argc, char **argv ){
  std::cout << argc << "\n";
  //if( argc != 65 ){ return 1; }

  CheckersBoard board(EmptyPieceLayout, CheckersBoard::SideType::White);

  for( int i = 1; i < argc; i++){
    int c = (i-1)%8;
    int r = (i-1)/8;

    //std::cout << r << " " << c << "\n";

    if( argv[i][0] == '1' ){
      board.SetPiece(Pos{c,r}, Piece::PieceType::White);
    }else if( argv[i][0] == '2'){
      board.SetPiece(Pos{c,r}, Piece::PieceType::Black);
    }

  }

  //board.SetPiece(Pos{0,2}, Piece::PieceType::White);
  //board.SetPiece(Pos{2,2}, Piece::PieceType::White);
  //board.SetPiece(Pos{4,2}, Piece::PieceType::White);
  //board.SetPiece(Pos{6,2}, Piece::PieceType::White);
  //board.SetPiece(Pos{6,0}, Piece::PieceType::White);



  //board.SetPiece(Pos{1,1}, Piece::PieceType::Black);
  //board.SetPiece(Pos{3,1}, Piece::PieceType::Black);
  //board.SetPiece(Pos{5,1}, Piece::PieceType::Black);
  //board.SetPiece(Pos{7,1}, Piece::PieceType::Black);

  AIPlayer aiPlayer;
  Move move = aiPlayer.ChooseBestMove(board);

  std::cout << move.from.row << " " << move.from.column << "\n";
  std::cout << move.to.row << " " << move.to.column << "\n";
  std::cout << "done\n";

  return 0;
}


/*
  Pos p1{ 0, 0 };
  Pos p2{ 1, 1 }; // p1 can jump p2
  Pos p3{ 4, 0 };

  board.SetPiece(p1, Piece::PieceType::White);
  board.SetPiece(p2, Piece::PieceType::Black);
  board.SetPiece(p3, Piece::PieceType::White);

  AIPlayer aiPlayer;
  Move move = aiPlayer.ChooseBestMove(board);
*/
