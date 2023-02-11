import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def distance(p1,p2):
	return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption('KMeans')

black = (0, 0, 0)
white = (255, 255, 255)
silver = (192, 192, 192)
#clusters's colors
red = (255, 0, 0)
green = (0, 128, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
lime = (0, 255, 0)
orange = (255, 127, 0)
magenta = (255, 0 ,255)
cyan = (0, 255, 255)

colors = [red, green, blue, yellow, purple, lime, orange, magenta, cyan]

font = pygame.font.SysFont('sans', 40)
font1 = pygame.font.SysFont('sans', 30)
font2 = pygame.font.SysFont('sans', 15)
text_plus = font.render('+', True, white)
text_minus = font.render('-', True, white)
text_run = font1.render('RUN', True, white)
text_random = font1.render('RANDOM', True, white)
text_algorithm = font1.render('ALGORITHM', True, white)
text_reset = font1.render('RESET', True, white)
text_error = font1.render('ERROR:', True, white)

K = 0
error = 0
points = []
clusters = []
labels = []
clock = pygame.time.Clock()
running = True

while running:
	clock.tick(60)
	screen.fill(black)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	#Draw interface
	#Draw panel
	pygame.draw.rect(screen, white, (10,10,1180,500))
	pygame.draw.rect(screen, black, (15,15,1170,490))

	#K button +
	pygame.draw.rect(screen, silver, (200,585,50,50))
	screen.blit(text_plus, (212,587))

	#K value
	pygame.draw.rect(screen, white, (100,585,100,50))
	pygame.draw.rect(screen, silver, (102,587,96,46))
	text_k = font1.render('K = ' + str(K), True, white)
	screen.blit(text_k, (110,592))

	#K button -
	pygame.draw.rect(screen, silver, (50,585,50,50))
	screen.blit(text_minus, (67,585))

	#Run button
	pygame.draw.rect(screen, white, (300,560,200,50))
	pygame.draw.rect(screen, silver, (302,562,196,46))
	screen.blit(text_run, (370,567))

	#Random button
	pygame.draw.rect(screen, white, (300,630,200,50))
	pygame.draw.rect(screen, silver, (302,632,196,46))
	screen.blit(text_random, (340,635))

	#Algorithm button
	pygame.draw.rect(screen, white, (600,560,200,50))
	pygame.draw.rect(screen, silver, (602,562,196,46))
	screen.blit(text_algorithm, (615,567))

	#Reset button
	pygame.draw.rect(screen, white, (600,630,200,50))
	pygame.draw.rect(screen, silver, (602,632,196,46))
	screen.blit(text_reset, (655,635))

	#Error text
	pygame.draw.rect(screen, white, (900,560,250,120))
	pygame.draw.rect(screen, silver, (902,562,246,116))
	screen.blit(text_error, (955,577))

	# Draw mouse position when mouse is in panel
	if 15 < mouse_x < 1185 and 15 < mouse_y < 505:
		text_mouse = font2.render("(" + str(mouse_x - 15) + "," + str(mouse_y - 15) + ")",True, white)
		screen.blit(text_mouse, (mouse_x + 15, mouse_y + 5))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Create point on panel
			if 15 < mouse_x < 1185 and 15 < mouse_y < 505:
				labels = []
				point = [mouse_x - 15, mouse_y - 15]
				points.append(point)

			#K button +
			if 200 < mouse_x < 250 and 585 < mouse_y < 635:
				if K < 9:
					K += 1

			#K button -
			if 50 < mouse_x < 100 and 585 < mouse_y < 635:
				if K > 0:
					K -= 1

			#Run button
			if 300 < mouse_x < 500 and 560 < mouse_y < 610:
				#Assign points to closet clusters
				labels = []
				if clusters == []:
					continue
				for p in points:
					distances_to_cluster = []
					for c in clusters:
						dist = distance(p,c)
						distances_to_cluster.append(dist)
					min_distance = min(distances_to_cluster)
					label = distances_to_cluster.index(min_distance)
					labels.append(label)

				#Update clusters
				for i in range(K):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1
					if count != 0:
						new_cluster_x = sum_x/count
						new_cluster_y = sum_y/count
						clusters[i] = [new_cluster_x, new_cluster_y]


			#Random button
			if 300 < mouse_x < 500 and 630 < mouse_y < 680:
				clusters = []
				labels = []
				for i in range(K):
					random_point = [randint(10,1180), randint(10,490)]
					clusters.append(random_point)

			#Algorithm button
			if 600 < mouse_x < 800 and 560 < mouse_y < 610:
				kmeans = KMeans(n_clusters=K).fit(points)
				labels = kmeans.predict(points)
				clusters = kmeans.cluster_centers_
				

			#Reset button
			if 600 < mouse_x < 800 and 630 < mouse_y < 680:
				points = []
				clusters = []
				labels = []

	# Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen,colors[i], (int(clusters[i][0]) + 10, int(clusters[i][1]) + 10), 10)

	# Draw point
	for i in range(len(points)):	
		pygame.draw.circle(screen,white, (points[i][0] + 15, points[i][1] + 15), 6)
		if labels == []:
			pygame.draw.circle(screen,white, (points[i][0] + 15, points[i][1] + 15), 5)
		else:
			pygame.draw.circle(screen,colors[labels[i]], (points[i][0] + 15, points[i][1] + 15), 5)

	# Calculate and draw error
	error = 0
	if clusters != [] and labels != []:
		for i in range(len(points)):
			error += distance(points[i], clusters[labels[i]])
	text_value_error = font1.render(str(int(error)), True, white)
	screen.blit(text_value_error, (970,625))

	pygame.display.flip()

pygame.quit()

