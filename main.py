from view.view import View
from control.game_manager import GameManager

view = View()
gm = GameManager(view=view)
view.mainloop()