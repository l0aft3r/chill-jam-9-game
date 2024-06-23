
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


class UpgradeButton():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, starfish, cost, lvl):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, False, self.base_color)
		self.starfish = starfish
		self.cost = cost
		self.level = lvl
		self.lvl = self.font.render(f'Required level: {self.level}',False, self.base_color)
		self.cost_text = self.font.render(f'{self.cost}', False, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		self.lvl = self.font.render(f'Required level: {self.level}',False, self.base_color)
		self.cost_text = self.font.render(f'{self.cost}', False, self.base_color)
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.starfish, (self.text_rect[0] - 17, self.text_rect[1]))
		screen.blit(self.cost_text, (self.text_rect[0] - 30, self.text_rect[1]))
		screen.blit(self.lvl, (self.text_rect[0] -30, self.text_rect[1] + 20))
		screen.blit(self.text, (self.text_rect[0] -30, self.text_rect[1] - 20))

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
