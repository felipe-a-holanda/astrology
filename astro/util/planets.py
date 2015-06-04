planets=[
'sun',
'moon',
'mercury',
'venus',
'mars',
'jupiter',
'saturn',
'uranus',
'neptune',
'pluto',
'mean_node',
'true_node',
'mean_apog',
'oscu_apog',
'earth',
'chiron',
'pholus',
'ceres',
'pallas',
'juno',
'vesta',
'intp_apog',
'intp_perg',
]

planets = planets[:10]
for i,p1 in enumerate(planets):
	for j,p2 in enumerate(planets):
		if j>i:
			d = {'id':'%s_%s_aspect' % (p1,p2)}
			print '<svg class="svg_aspect"><line id="{id}" x1="0" y1="0" x2="0" y2="0" style="stroke:rgb(0,0,0);stroke-width:0"></line></svg>'.format(**d)

