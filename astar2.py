import heapq

class Cell(object):                                                              ##defining cell as a object with values 
	def __init__(self,x,y,reachable):                                            ##x and y are co-ordinates
		self.reachable=reachable
		self.x=x
		self.y=y
		self.parent=None
		self.g=0
		self.h=0
		self.f=0
		
class AStar(object):                                                            ##defining grid and its parameters
	def __init__(self):
		self.opened=[]
		heapq.heapify(self.opened)
		self.closed=set()
		self.grid_height=6
		self.grid_width=6
		
	def init_grid(self):                                                     ##initializing grid alongwith the wall cells
		walls=((0,5),(1,0),(1,1),(1,2),(1,5),(2,3),(3,1),(3,2),(3,5),(4,1),(4,4),(5,1))
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				if(x,y) in walls:
					reachable=False
				else:
					reachable=True
					self.cells.append(Cell(x,y,reachable))
					self.start=self.get_cell(0,0)
					self.end=self.get_cell(5,5)
						
	def get_heuristic(self,cell):
		return 10*(abs(cell.x-self.end.x)+abs(cell.y-self.end.y))
			
			
	def get_cell(self,x,y):
		return self.cells[x*self.grid_height+y]
			
	def get_adjacent_cells(self,cell):                                               ##method to retrieve adjacent cells
			
		cells=[]
		if cell.x<self.grid_width-1:
			cells.append(self.get_cell(cell.x+1,cell.y))
		if cell.y>0:
			cells.append(self.get_cell(cell.x,cell.y-1))
		if cell.x>0:
			cells.append(self.get_cell(cell.x-1,cell.y))
		if cell.y<self.grid_height-1:
			cells.append(self.get_cell(cell.x,cell.y+1))
		return cells
			
	def display_path(self):                                                      ##method to print the path
		cell=self.end
		while cell.parent is not self.start:
			cell=cell.parent
			print 'path:cell:%d,%d'%(cell.x,cell.y)
				
	def update_cell(self,adj,cell):                                               ##method to calculate g and h values
		adj.g=cell.g+10
		adj.h=self.get_hueristic(adj)
		adj.parent=cell
		adj.f=adj.h+adj.g
			
	def process(self):                                                             ##implementation of algorithm
		heapq.heappush(self.opened,(self.start.f,self.start))
		while len(self.opened):
			f,cell=heapq.heappop
			(self.opened)
			self.closed.add(cell)
			if cell is self.end:
				self.display_path()
				break
			adj_cells=self.get_adjacent_cells(cell)
			for adj_cell in adj_cells:
				if adj_cell.reachable and adj_cell not in self.closed:
					if (adj_cell.f,adj_cell) in self.opened:
						if adj_cell.g>cell.g+10:
							self.update_cell(adj_cell,cell)
						else:
							self.update_cell(adj_cell,cell)
							heapq.heappush(self.opened,(adj_cell.f,adj_cell))