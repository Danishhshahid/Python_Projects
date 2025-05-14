import streamlit as st
import time
from game import TicTacToe
from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer

# Set page config
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 24px;
        font-weight: bold;
    }
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    # Initialize all session state variables at once
    defaults = {
        'board': TicTacToe(),
        'current_player': 'X',
        'game_over': False,
        'winner': None,
        'player_type': 'Human',
        'game_history': []
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def render_board():
    board = st.session_state.board.board
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            with cols[j]:
                button_text = board[index] if board[index] != ' ' else ''
                button_color = "green" if board[index] == 'X' else "red" if board[index] == 'O' else "white"
                if st.button(
                    button_text,
                    key=f'btn_{index}',
                    disabled=st.session_state.game_over or board[index] != ' ',
                    help=f"Position {index}"
                ):
                    make_move(index)

def make_move(square):
    if st.session_state.board.make_move(square, st.session_state.current_player):
        if st.session_state.board.current_winner:
            st.session_state.game_over = True
            st.session_state.winner = st.session_state.current_player
            st.session_state.game_history.append(f"Player {st.session_state.current_player} wins!")
        elif not st.session_state.board.empty_square():
            st.session_state.game_over = True
            st.session_state.winner = 'tie'
            st.session_state.game_history.append("Game ended in a tie!")
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            if st.session_state.player_type == 'Computer' and st.session_state.current_player == 'O':
                time.sleep(0.5)
                computer_move()

def computer_move():
    if not st.session_state.game_over:
        computer = GeniusComputerPlayer('O')
        square = computer.get_move(st.session_state.board)
        make_move(square)

def reset_game():
    st.session_state.board = TicTacToe()
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def main():
    # Initialize session state first
    initialize_session_state()
    
    st.title("🎮 Tic Tac Toe")
    
    # Sidebar for game settings
    with st.sidebar:
        st.header("Game Settings")
        player_type = st.radio("Select opponent type:", ["Human", "Computer"])
        st.session_state.player_type = player_type
        
        if st.button("Reset Game"):
            reset_game()
            st.rerun()
        
        st.header("Game History")
        # Safely access game history
        if hasattr(st.session_state, 'game_history') and st.session_state.game_history:
            for result in st.session_state.game_history[-5:]:  # Show last 5 games
                st.write(result)
        else:
            st.write("No games played yet")
    
    # Game status
    status_container = st.empty()
    if st.session_state.winner:
        if st.session_state.winner == 'tie':
            status_container.info("It's a tie! 🤝")
        else:
            status_container.success(f"Player {st.session_state.winner} wins! 🎉")
    else:
        status_container.info(f"Current player: {st.session_state.current_player}")
    
    # Render the game board
    render_board()
    
    # Game instructions
    with st.expander("How to Play"):
        st.markdown("""
        1. The game is played on a 3x3 grid
        2. Players take turns placing their mark (X or O) in an empty square
        3. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins
        4. If all squares are filled and no player has won, the game is a tie
        """)

if __name__ == "__main__":
    main() 