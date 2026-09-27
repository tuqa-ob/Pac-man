from pm_game.adapter import MazeAdapter


def test_generate_maze() -> None:
    """Test that the adapter generates a 20x20 maze."""
    adapter = MazeAdapter(width=20, height=20, seed=42)

    adapter.generate()

    assert len(adapter.maze) == 20
    assert len(adapter.maze[0]) == 20
