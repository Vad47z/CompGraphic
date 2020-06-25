from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk
import datetime

class Lab1():
	def __init__(self):
		self.channels = dict()
		self.samples_number = 0
		self.sampling_rate = 0
		self.start_date = ""
		self.start_time = ""
		self.datetime = ""
		self.file_name = ""
		

		self.root = Tk()
		self.navigation_window = ""
		self.navigation_window_temp = []
		self.oscillogram_main = ""
		self.oscillogram_main_temp = []

		self.oscillogram_main_start = 0
		self.oscillogram_main_end = 0

		self.root.geometry('800x600')
		self.root.title("DSP-Shipkov")

		self.main_menu = Menu(self.root) 
		self.root.config(menu=self.main_menu, background="#808080") 

		#Файл
		self.file_menu = Menu(self.main_menu, tearoff=0)
		self.file_menu.add_command(label="Открыть", command=self.open_file)
		self.file_menu.add_command(label="Сохранить", command=self.save_file)

		#Инструменты
		self.tools_menu = Menu(self.main_menu, tearoff=0)
		self.tools_menu.add_command(label="Информация о сигнале", command=self.tools_info)
		self.tools_menu.add_command(label="Окно навигации", command=self.signal_display)
		self.tools_menu.add_command(label="Фрагмент", command=self.fragment_change)

		#Моделирование
		self.model_menu = Menu(self.main_menu, tearoff=0)

		#Фильтрация
		self.filter_menu = Menu(self.main_menu, tearoff=0)

		#Анализ
		self.analysis_menu = Menu(self.main_menu, tearoff=0)

		#Настройки
		self.settings_menu = Menu(self.main_menu, tearoff=0)

		#Справка
		self.help_menu = Menu(self.main_menu, tearoff=0) 
		self.help_menu.add_command(label="О программе", command=self.about)

		self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
		self.main_menu.add_cascade(label="Инструменты", menu=self.tools_menu)
		self.main_menu.add_cascade(label="Моделирование", menu=self.model_menu)
		self.main_menu.add_cascade(label="Фильтрация", menu=self.filter_menu)
		self.main_menu.add_cascade(label="Анализ", menu=self.analysis_menu)
		self.main_menu.add_cascade(label="Настройки", menu=self.settings_menu)
		self.main_menu.add_cascade(label="Справка", menu=self.help_menu)

		self.root.mainloop() 

	#Окрытие файла и обработка информации из него
	def open_file(self):
		try:
			file_name = fd.askopenfilename(filetypes=(("TXT files", "*.txt"),))
			if file_name != "":
				f = open(file_name)
				temp = f.read().split('\n')

				self.file_name = file_name
				self.samples_number = int(temp[3])
				self.sampling_rate = float(temp[5])
				self.start_date = temp[7]
				self.start_time = temp[9]
				self.datetime = datetime.datetime(*map(lambda x: int(x), self.start_date.split('-')[::-1]), int(self.start_time.split(':')[0]), int(self.start_time.split(':')[1]), int(self.start_time.split(':')[2].split('.')[0]), int(self.start_time.split(':')[2].split('.')[1])) 
				
				self.navigation_window = ""
				self.navigation_window_temp = []
				self.oscillogram_main = ""
				self.oscillogram_main_temp = []

				#проверка на присутствие ';' в конце списка имён каналов
				if temp[11].split(';')[-1] == '':
					temp_ = temp[11].split(';')
					temp_.pop()
					self.channels = dict.fromkeys(temp_, [])
				else:
					self.channels = dict.fromkeys(temp[11].split(';'), [])

				temp.remove("")
				temp_ = temp[12:]

				temp = []
				for i in temp_:
					temp.extend(i.split())


				for i, channel in enumerate(self.channels.keys()):
					self.channels[channel] = temp[i:len(temp):len(self.channels.keys())]



				f.close()

				self.signal_display(600, 200)
		except Exception as e:
			mb.showerror(title="Ошибка", message=e)
			print(e)

	#Сохранение файла
	def save_file(self):

		def save():
			channels = [i[0] for i in list(filter(lambda x: x[1].get() == True, var))]

			if channels != []:
				if (min_sample.get().isdigit() and max_sample.get().isdigit()):
					if (int(min_sample.get()) <= int(max_sample.get())) and (int(min_sample.get()) > 0 and int(max_sample.get()) <= int(self.samples_number)): 

						#смещение по времени с учётом смещения отрезка
						start_datetime = self.datetime + datetime.timedelta(seconds=int(min_sample.get())-1)
						start_date = "-".join(str(start_datetime.date()).split('-')[::-1])
						start_time = start_datetime.time()

						info = "# channels number \n%s\n" % (len(channels))
						info += "# samples number \n%s\n" % (int(max_sample.get())-int(min_sample.get())+1)
						info += "# sampling rate \n%s\n" % (self.sampling_rate)
						info += "# start date \n"+start_date+"\n"
						info += "# start time \n"+str(start_time)+"."+str(start_time.microsecond)+"\n"
						info += "# channels names\n" + ";".join(channels) + "\n"

						file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),))
						
						if file_name != "":
							f = open(file_name+".txt", 'w')

							f.write(info)

							for i in range(int(min_sample.get())-1, int(max_sample.get())):
								temp_ = ""
								for j in channels:
									temp_ += self.channels[j][i]+" "
								temp_ += "\n"

								f.write(temp_)

							f.close()
							save_settings.destroy()
					else:
						mb.showerror(title="Ошибка", message="Ошибка в отсчётах")
				else:
					mb.showerror(title="Ошибка", message="Ошибка в отсчётах")
			else:
				mb.showerror(title="Ошибка", message="Не выбран ни один канал")




		if self.sampling_rate == 0 and self.samples_number == 0:
			mb.showinfo("Текущее состояние многоканального сигнала", "Нет информации")
		else:
			save_settings = Toplevel()
			save_settings.title = "Настройки сохранения"

			label = Label(save_settings, text="Каналы", font="arial 12")
			label.grid(row=0,column=0)

			var = list()

			for i, channel in enumerate(self.channels.keys()):
				var.append((channel, BooleanVar()))
				check = Checkbutton(save_settings, text=channel, variable=var[i][1], onvalue=1, offvalue=0)
				check.grid(row=i+1,column=0)

			label = Label(save_settings, text="\nОтсчёты (мин.: 1; макс.: %s)" % self.samples_number, font="arial 12")
			label.grid(row=0,column=2,columnspan=2)

			min_sample = StringVar()
			min_sample.set("1")
			max_sample = StringVar()
			max_sample.set(str(self.samples_number))

			label = Label(save_settings, text="От:", font="arial 12")
			entry = Entry(save_settings, textvariable=min_sample)
			label.grid(row=1,column=2)
			entry.grid(row=1,column=3)

			label = Label(save_settings, text="До:", font="arial 12")
			entry = Entry(save_settings, textvariable=max_sample)
			label.grid(row=3,column=2)
			entry.grid(row=3,column=3)

			btn = Button(save_settings,text='ОК',width=5,height=2,command=save)
			btn.grid(row=len(self.channels.keys())+2,column=2)

			save_settings.grab_set()
			save_settings.resizable(False, False)

	#Вывод информации о сигнале
	def tools_info(self):
		if self.sampling_rate == 0 and self.samples_number == 0:
			mb.showinfo("Текущее состояние многоканального сигнала", "Нет информации, попробуйте открыть файл")
		else:
			info_window = Toplevel()
			info_window.title("Текущее состояние многоканального сигнала")

			temp_time = datetime.timedelta(seconds=(1/self.sampling_rate)*self.samples_number)
			end_datetime = self.datetime+temp_time

			info = "Общее число каналов - "+str(len(self.channels.keys()))+'\n'
			info += "Общее число отсчётов - "+str(self.samples_number)+'\n'
			info += "Частота дискретизации - "+str(self.sampling_rate)+" Гц (шаг между отсчётами "+str(round(1/self.sampling_rate, 3))+" сек)"+'\n'
			info += "Дата и время начала записи - %s-%s-%s %s:%s:%s.%s \n" % (self.datetime.day, self.datetime.month, self.datetime.year, self.datetime.hour, self.datetime.minute, self.datetime.second, self.datetime.microsecond)
			info += "Дата и время окончания записи - %s-%s-%s %s:%s:%s.%s \n" % (end_datetime.day, end_datetime.month, end_datetime.year, end_datetime.hour, end_datetime.minute, end_datetime.second, end_datetime.microsecond)
			info += "Длительность - %s - суток, %s - часов, %s - минут, %s.%s - секунд \n" % (temp_time.days, temp_time.seconds//3600, (temp_time.seconds//60)%60, temp_time.seconds-(temp_time.seconds//3600)*3600-((temp_time.seconds//60)%60)*60, temp_time.microseconds)
			info += "\nИнформация о каналах\n"

			cols = ("N", "Имя", "Источник")
			table = ttk.Treeview(info_window, columns=cols, show='headings')
			for col in cols:
				table.heading(col, text=col)
			table.column("N", width=40, minwidth=40, stretch=False)
			table.column("Имя", width=120, minwidth=120, stretch=False)
			table.column("Источник", width=250, minwidth=250, stretch=False)
			for i, channel in enumerate(self.channels.keys()):
				table.insert("", "end", values=(i+1, channel, self.file_name.split('/')[-1]))

			label1 = Label(info_window, text=info, font="arial 12")
			label2 = Label(info_window, text="Активный фрагмент: [], всего отсчётов - "+str(self.samples_number), font="arial 12")

			label1.pack()
			table.pack()
			label2.pack()
			info_window.grab_set()
			info_window.resizable(False, False)

	#Вывод информации о программе
	def about(self):
		mb.showinfo(title="О программе", message="Программу разработал студент группы Б8117-02.03.01\n Шипков Вадим")


	#Отображение окна навигации
	def signal_display(self, x=0, y=0):
		if self.sampling_rate == 0 and self.samples_number == 0:
			mb.showinfo("Окно навигации", "Нет информации, попробуйте открыть файл")
		else:
			if self.sampling_rate == 0 and self.samples_number == 0:
				mb.showinfo("Окно навигации", "Нет информации, попробуйте открыть файл")
			else:
				try:
					self.navigation_window.destroy()
					self.navigation_window_temp = []
				except:
					pass

				self.navigation_window = Toplevel(self.root)
				self.navigation_window.title("Окно навигации")
				
				canvas_width = 150
				canvas_height = 40

				#обновление окна навигации с сохранением его расположения
				btn = Button(self.navigation_window, text="Обновить", command=lambda: self.signal_display(self.navigation_window.winfo_rootx()-10, self.navigation_window.winfo_rooty()-30))
				btn.pack()
				
				for i in self.channels.keys():
					#mean = sum(map(lambda x: float(x), self.channels[i]))/len(self.channels[i])
					#хз зачем, но для чего-то же делал 

					self.oscillogram_display(self.navigation_window, self.navigation_window_temp, i, canvas_width, canvas_height, 0)



				self.navigation_window.resizable(False, False)
				self.navigation_window.attributes("-toolwindow", True)
				self.navigation_window.transient(self.root)
				#self.navigation_window.tkraise(self.root)

				self.navigation_window.geometry("+"+str(x)+"+"+str(y))

	#выбор отображаемого фрагмента сигнала
	def fragment_change(self):
		if self.sampling_rate == 0 and self.samples_number == 0:
			mb.showinfo("Временной диапозон", "Нет информации, попробуйте открыть файл")
		else:
			fragment = Toplevel()
			fragment.title = "Временной диапозон"

			label = Label(fragment, text="\nОтсчёты (мин.: 1; макс.: %s)" % self.samples_number, font="arial 12")
			label.grid(row=0,column=2,columnspan=2)

			min_sample = StringVar()
			min_sample.set("1")
			max_sample = StringVar()
			max_sample.set(str(self.samples_number))

			label = Label(fragment, text="От:", font="arial 12")
			entry = Entry(fragment, textvariable=min_sample)
			label.grid(row=1,column=2)
			entry.grid(row=1,column=3)

			label = Label(fragment, text="До:", font="arial 12")
			entry = Entry(fragment, textvariable=max_sample)
			label.grid(row=3,column=2)
			entry.grid(row=3,column=3)

			btn = Button(fragment,text='Ok',width=5,height=2,command=lambda: self.oscillogram_main_change(min_sample, max_sample))
			btn.grid(row=len(self.channels.keys())+2,column=2)

			fragment.grab_set()
			fragment.resizable(False, False)



	#Отрисовка осциллограммы
	def oscillogram_display(self, obj, obj_temp, channel_name, canvas_width, canvas_height, window, start = 0, end = 0):
			
		label = Label(obj, width = canvas_width+10, height = canvas_height+10, bg = "#808080")
		label1 = Label(label, bg = "white", text = str(channel_name))
		canv = Canvas(label, width = canvas_width, height = canvas_height, bg = "white", cursor = "arrow")
			
		temp = [*map(lambda x: float(x), self.channels[channel_name])]
		
		mx = max(temp)
		k = (mx-min(temp))/canvas_height

		#если значений меньше, чем ширина отрисовки
		if len(temp) < canvas_width:
			step = ((canvas_width)//len(temp))
			rem = (canvas_width)%len(temp)

			last_value = 0
			#если k равен 0, то изменений в графике не будет вообще (просто прямая)
			if (k != 0):
				for j in range(1, canvas_width//step):

					value1 = temp[j-1] #доработать тк вызывается последний элемент
					value2 = temp[j]
					canv.create_line(j*(step+(step/(canvas_width//step))), (mx-value1)/k, (j+1)*(step+(step/(canvas_width//step))), (mx-value2)/k)

					last_value = value2

				if (rem != 0):
					#отрисовка остатка

					value1 = last_value
					value2 = sum(temp[(canvas_width-1)*step:((canvas_width-1)*step)+rem])/rem

					canv.create_line(j, (mx-value1)/k, j+1, (mx-value2)/k)
			else:
				canv.create_line(0, canvas_height//2, canvas_width, canvas_height//2)
		else:
			step = len(temp)//(canvas_width-1)
			rem = len(temp)%(canvas_width-1)

			last_value = 0

			#если k равен 0, то изменений в графике не будет вообще (просто прямая)
			if (k != 0):
				for j in range(canvas_width-1): #мб ошибка и надо -2 а не -1

					value1 = sum(temp[j*step:(j+1)*step])/step
					value2 = sum(temp[(j+1)*step:(j+2)*step])/step

					canv.create_line(j, (mx-value1)/k, j+1, (mx-value2)/k)

					last_value = value2

				if (rem != 0):
					#отрисовка остатка

					value1 = last_value
					value2 = sum(temp[(canvas_width-1)*step:((canvas_width-1)*step)+rem])/rem

					canv.create_line(j, (mx-value1)/k, j+1, (mx-value2)/k)
			else:
				canv.create_line(0, canvas_height//2, canvas_width, canvas_height//2)


		if window == 0:
			canv.bind("<Button-3>", lambda x: self.nav_display_menu(x, channel_name))
		elif window == 1:
			canv.bind("<Button-3>", lambda x: self.osc_display_menu(x, channel_name))
		label.pack()
		canv.pack()	
		label1.pack()
		obj_temp.append([channel_name, label, label1, canv])

	#Отображение выпадающего списка при нажатии ПКМ в навигационном окне
	def nav_display_menu(self, event, channel):
		menu = Menu(tearoff=0)


		menu.add_command(label="Осциллограмма", command=lambda: self.oscillogram_main_display(channel, 300, 200))
		menu.post(event.x_root, event.y_root)

	#Отображение выпадающего списка при нажатии ПКМ в осциллограммах
	def osc_display_menu(self, event, channel):
		menu = Menu(tearoff=0)


		menu.add_command(label="Закрыть", command=lambda: self.oscillogram_main_display(channel, 300, 200))
		menu.post(event.x_root, event.y_root)

	#Отображения основных осциллограмм
	def oscillogram_main_display(self, channel, x, y):
		if self.sampling_rate == 0 and self.samples_number == 0:
			mb.showinfo("Осциллограммы", "Нет информации, попробуйте открыть файл")
		else:
			canvas_width = 600
			canvas_height = 100

			def oscillogram_main_clear():
				self.oscillogram_main_temp = []
				self.oscillogram_main.destroy()
				self.oscillogram_main = ""

			if self.oscillogram_main_temp == []:
				self.oscillogram_main = Toplevel(self.root)
				self.oscillogram_main.title("Осциллограммы")
				self.oscillogram_main.protocol("WM_DELETE_WINDOW", oscillogram_main_clear)
				
				#menu = Menu(tearoff=0)
				#menu.add_command(label="Обновить", command=lambda: self.oscillogram_main_display(self.oscillogram_main.winfo_rootx()-10, self.oscillogram_main.winfo_rooty()-30))
				#self.oscillogram_main.config(menu=menu)

				self.oscillogram_display(self.oscillogram_main, self.oscillogram_main_temp, channel, canvas_width, canvas_height, 1)



				self.oscillogram_main.resizable(False, False)
				self.oscillogram_main.transient(self.root)
				#self.navigation_window.tkraise(self.root)

				self.oscillogram_main.geometry("+"+str(x)+"+"+str(y))
			else:
				flag = 0
				for i, k in enumerate(self.oscillogram_main_temp):
					if channel == k[0]:
						for j in self.oscillogram_main_temp[i][1:]:
							j.destroy()
						self.oscillogram_main_temp.pop(i)
						flag = 1
						break
				if flag == 0:
					self.oscillogram_display(self.oscillogram_main, self.oscillogram_main_temp, channel, canvas_width, canvas_height, 1)
					self.oscillogram_main_temp.append(channel)


	#Отображение основных осциллограмм после изменения диапозона
	def oscillogram_main_change(self, start, end):

		if (start.get().isdigit() and end.get().isdigit()):
			if (int(start.get()) <= int(end.get())) and (int(start.get()) > 0 and int(end.get()) <= int(self.samples_number)): 


				print(start.get())
				print(end.get())
			else:
				mb.showerror("Ошибка", "Введены неверные данные")
		else:
			mb.showerror("Ошибка", "Введены не числа")

test = Lab1()