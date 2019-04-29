cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

set(LIBRARY_NAME CheckersEngine)
project(${LIBRARY_NAME})

add_library(${LIBRARY_NAME}
  AIPlayer.h
  AIPlayer.cpp
  CheckersBoard.h
  CheckersBoard.cpp
  CheckersBoardNode.h
  Move.h
  Piece.h
  Pos.h
)

target_include_directories (${LIBRARY_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}\\src)

target_link_libraries(${LIBRARY_NAME} ${EXTRA_LIBS})


add_executable( engine
  engine.cpp
  )

target_link_libraries( engine CheckersEngine )

