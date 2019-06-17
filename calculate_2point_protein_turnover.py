import pandas as pd
import os
import csv
import statistics


def prompt():
    print('\n')
    print('Please make sure the folder path that contains your data does not contain any spaces. I.e C:\Kasumov lab\Andrew\Data_Folder will not work because there is a space in "Kasumov lab".')
    print('Please enter the path of the folder that contains your files. I.e C:\Kasumov_lab\Andrew\Data_Folder')
    folder_name = input('Folder Path: ').strip()
    while os.path.isdir(folder_name) == False:
    	print('This is an invalid directory, please try again.')
    	print('\n')
    	print('Please make sure the folder path that contains your data does not contain any spaces. I.e C:\Kasumov lab\Andrew\Data_Folder will not work because there is a space in "Kasumov lab".')
    	print('Please enter the path of the folder that contains your files. I.e C:\Kasumov_lab\Andrew\Data_Folder')
    	folder_name = input('Folder Path: ').strip()
    
    print('\n')
    print('Please select from the following choices.')
    print('1. Use M0 and M1 to calculate FSR.')
    print('2. Use M0-M2 to calculate FSR.')
    print('3. Use M0-M3 to calculate FSR.')
    print('4. Use M0-M4 to calculate FSR.')
    fsr_selection = input('Enter your choice: ').strip()
    while check_fsr_input(fsr_selection)== False:
        print('\n')
        print('This is an invalid input.')
        print('Please try again.')
        print('\n')
        print('Please select from the following choices.')
        print('1. Use only M0 and M1 to calculate FSR.')
        print('2. Use M0-M2 to calculate FSR.')
        print('3. Use M0-M3 to calculate FSR.')
        print('4. Use M0-M4 to calculate FSR.')
        fsr_selection = input('Enter your choice: ').strip()
    
    print('\n')
    print('Please enter the number of 0 timepoints in the dataset. For example if there is 1 sample in duplicate please enter 2.')
    number_of_zeros = input('Enter now: ').strip()
    while check_number(number_of_zeros) == False:
    	print('\n')
    	print('This is an incorrect input.')
    	print('Please try again.')
    	print('Please enter the number of 0 timepoints in the dataset. For example if there is 1 sample in duplicate please enter 2.')
    	number_of_zeros = input('Enter now: ').strip()
    number_of_zeros = int(number_of_zeros)
    
    print('\n')
    print('Please enter the number of T2 timepoints in the dataset. For example if there are 2 samples in duplicate please enter 4.')
    number_of_T2 = input('Enter now: ').strip()
    while check_number(number_of_T2) == False:
    	print('\n')
    	print('This is an incorrect input.')
    	print('Please try again.')
    	print('Please enter the number of T2 timepoints in the dataset. For example if there are 2 samples in duplicate please enter 4.')
    	number_of_T2 = input('Enter now: ').strip()
    number_of_T2 = int(number_of_T2)
    
    print('\n')
    print('Please enter the body water enrichment for each of your samples separated by commmas.')
    print('For example if you have 2 zero sample and 2 T2. Please enter 4 numbers.')
    print('Ex: 0,0,2.5,2.5')
    bwe = input('Enter now: ').strip()
    while len(bwe.split(',')) != (number_of_zeros + number_of_T2):
    	print('\n')
    	print('The numbers you have entered do not match your input for number of zeros and T2. Please double-check your entry.')
    	print('Please enter the body water enrichment for each of your samples separated by commmas.')
    	print('For example if you have 2 zero sample and 2 T2. Please enter 4 numbers.')
    	print('Ex: 0,0,2.5,2.5')
    	bwe = input('Enter now: ').strip()

    print('\n')
    print('Please enter the time points for each of your samples separated by commmas.')
    print('For example if you have 2 zero sample and 2 T2. Please enter 4 numbers.')
    print('Ex: 0,0,10,10')
    user_time_points = input('Enter now: ').strip()
    while len(user_time_points.split(',')) != (number_of_zeros + number_of_T2):
    	print('\n')
    	print('The numbers you have entered do not match your input for number of zeros and T2. Please double-check your entry.')
    	print('Please enter the body water enrichment for each of your samples separated by commmas.')
    	print('For example if you have 2 zero sample and 2 T2. Please enter 4 numbers.')
    	print('Ex: 0,0,2.5,2.5')
    	user_time_points = input('Enter now: ').strip()

    return folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points

def check_number(number):
	try:
		int(number)
	except ValueError:
		return False
	else:
		return True

def check_fsr_input(fsr_selection):
	if fsr_selection == '1' or fsr_selection == '2' or fsr_selection == '3' or fsr_selection == '4':
		return True
	else:
		return False

def read_file_FSR(folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points):
	for file_name in os.listdir(folder_name): #folder_name is actually the path to the folder
		file_name_split = file_name.split('.')
		if len(file_name_split) < 2:
		    pass
		elif file_name_split[1] == 'Quant':
		    file_path = os.path.sep.join([folder_name, file_name])
		    with open(file_path) as file:
		        rows_counter = 1
		        for rowrow in file:
		            if rows_counter == 1:
		                pass
		            elif rows_counter == 2:
		                rowrow = rowrow.split(',')
		                if rowrow[0] == 'Peptide':
		                    read_data_A2_FSR(file, file_name, file_path, folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points)
		                else:
		                    pass
		            elif rows_counter == 4:
		                rowrow = rowrow.split(',')
		                if rowrow[0] == 'Peptide':
		                    read_data_A4_FSR(file, file_name, file_path, folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points)
		                else:
		                    pass
		            else:
		                pass
		            rows_counter += 1
		else:
		    pass
def read_data_A2_FSR(file, file_name, file_path, folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points):
	time_point_list = []
	column_list = create_columns(user_time_points)
	df = pd.DataFrame(columns = column_list)
	with open(file_path) as file:
		csv_reader = csv.reader(file)
		for index, row in enumerate(csv_reader, 1):
			if index == 1:#Making the Timepoints
				for i in row:
					if len(i.strip())>2:
						time_point_list.append(i.strip())
					else:
						pass
			elif index == 2:
				data_locations = []
				for position,value in enumerate(row):
				    if value.strip() == 'I0' or value.strip() == 'I1' or value.strip() == 'I2' or value.strip() == 'I3' or value.strip() == 'I4' or value.strip() == 'I5' :
				        data_locations.append(position)
				    if value.strip() == 'Charge':
				    	charge_position = position
				    if value.strip() == 'SeqMass':
				        SeqMass_position = position
				    else:
				        pass
				data_locations = data_locations[:number_of_zeros*6] + data_locations[number_of_T2*-6:] #Only keeps data for the zeros and T2
			else:
				temp_list = []
				row[0] = row[0] + str(index)#Creates unique peptide name
				temp_list.append(row[0].strip())#Adds the peptide
				temp_list.append(row[charge_position])
				temp_list.append(row[SeqMass_position])
				for i in data_locations:
				    temp_list.append(row[i])

				temp_df = pd.DataFrame([temp_list], columns = column_list)
				df = df.append(temp_df)
				df = df.set_index(df['Peptides'])
	
		final_file_name = '{}_twotimepoints_option{}.xlsx'.format(file_name.split('.')[0], fsr_selection)
		final_file_path = os.path.sep.join([folder_name, final_file_name])
		
		if fsr_selection == '1':
			final_data_df = calculate_FSR_selection_1(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		elif fsr_selection == '2':
			final_data_df = calculate_FSR_selection_2(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		elif fsr_selection == '3':
			final_data_df = calculate_FSR_selection_3(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		elif fsr_selection == '4':
			final_data_df = calculate_FSR_selection_4(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		
		final_data_df.to_excel(final_file_path, index = False)
	   	
def read_data_A4_FSR(file, file_name, file_path, folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points):
	time_point_list = []
	column_list = create_columns(user_time_points)
	df = pd.DataFrame(columns = column_list)
	with open(file_path) as file:
		csv_reader = csv.reader(file)
		for index, row in enumerate(csv_reader, 1):
			if index == 1 or index == 2:
				pass
			elif index == 3:#Making the Timepoints
				for i in row:
					if len(i.strip())>2:
						time_point_list.append(i.strip())
					else:
						pass
			elif index == 4:
				data_locations = []
				for position,value in enumerate(row):
				    if value.strip() == 'I0' or value.strip() == 'I1' or value.strip() == 'I2' or value.strip() == 'I3' or value.strip() == 'I4' or value.strip() == 'I5' :
				        data_locations.append(position)
				    if value.strip() == 'Charge':
				    	charge_position = position
				    if value.strip() == 'SeqMass':
				        SeqMass_position = position
				    else:
				        pass
				data_locations = data_locations[:number_of_zeros*6] + data_locations[number_of_T2*-6:] #Only keeps data for the zeros and T2
			else:
				temp_list = []
				row[0] = row[0] + str(index)#Creates unique peptide name
				temp_list.append(row[0].strip())#Adds the peptide
				temp_list.append(row[charge_position])
				temp_list.append(row[SeqMass_position])
				for i in data_locations:
				    temp_list.append(row[i])

				temp_df = pd.DataFrame([temp_list], columns = column_list)
				df = df.append(temp_df)
				df = df.set_index(df['Peptides'])
	
		final_file_name = '{}_twotimepoints_option{}.xlsx'.format(file_name.split('.')[0], fsr_selection)
		final_file_path = os.path.sep.join([folder_name, final_file_name])
		
		if fsr_selection == '1':
			final_data_df = calculate_FSR_selection_1(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		elif fsr_selection == '2':
			final_data_df = calculate_FSR_selection_2(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		elif fsr_selection == '3':
			final_data_df = calculate_FSR_selection_3(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		elif fsr_selection == '4':
			final_data_df = calculate_FSR_selection_4(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2)
		
		final_data_df.to_excel(final_file_path, index = False)
	   	
def calculate_FSR_selection_1(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2):
	import math
	final_data_df = pd.DataFrame()
	
	t = float(user_time_points.split(',')[-1])
	k_format = 'k({})'.format(t)
	temporary_list = [k_format for i in range(number_of_T2)]
	final_data_df['peptide'] = temporary_list
		
	X2 = 0.00015
	X1 = 1-X2
	Y20 = X2/X1
	bwe_split = bwe.split(',')[-number_of_T2:]
	
	for peptide, row in df.iterrows():
		temp_k = []
		N = calculate_N(peptide, fsr_selection)
		V0 = calculate_V0_selection1(df, row, number_of_zeros)
		V1_yield = calculate_V1_selection1(df, row, number_of_T2)
		for index, V1 in enumerate(V1_yield):
			if V1 == 0:
				temp_k.append('')
			else:
				D2 = float(bwe_split[index])/100
				Y21 =D2/(1-D2)
				P =1 -  (1/((1/(1-V0))+ N*(Y21 - Y20)))
				try:
					k = (-1/t)*math.log(1-((V1-V0)/(P-V0)))	
				except ValueError:
					k = ''	
				finally:
					temp_k.append(k)
		final_data_df[peptide] = pd.Series(temp_k)
	return final_data_df

def calculate_V0_selection1(df, row, number_of_zeros):
	temp_V0 = []
	for i in range(number_of_zeros):
		#Position 0 =charge, position 1= mass, position 2=M0
		# M0 = float(row[i*6+3].strip())
		# M1 = float(row[i*6+4].strip())
		try:
			temp_V0.append(float(row[i*6+4].strip())/(float(row[i*6+4].strip())+float(row[i*6+3].strip())))
		except ZeroDivisionError:
			pass
		except ValueError:
			pass
		try:
			V0 = statistics.mean(temp_V0)
		except:
			V0 = 0
		return V0

def calculate_V1_selection1(df, row, number_of_T2):
	temp_peptide = row[number_of_T2*-6:]
	for i in range(number_of_T2):
		#M0 = float(temp_peptide[i*6].strip())
		#M1 = float(temp_peptide[i*6+1].strip())
		try:
			V1_yield = float(temp_peptide[i*6+1].strip())/ (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6].strip()))
		except ZeroDivisionError:
			V1_yield = 0
		except ValueError:
			V1_yield = 0
		finally:
			yield V1_yield

def calculate_FSR_selection_2(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2):
	import math
	final_data_df = pd.DataFrame()
	
	t = float(user_time_points.split(',')[-1])
	k_format = 'k({})'.format(t)
	temporary_list = [k_format for i in range(number_of_T2)]
	final_data_df['peptide'] = temporary_list
		
	X2 = 0.00015
	X1 = 1-X2
	Y20 = X2/X1
	Y13 = 0.011074/(1-0.011074)
	Y15 = (1-0.99635)/0.99635
	Y17 = 0.00037/0.99759
	Y33 = 0.0076/0.95

	bwe_split = bwe.split(',')[-number_of_T2:]
	for peptide, row in df.iterrows():
		temp_k = []
		N = calculate_N(peptide, fsr_selection)
		Cp, Hs, Np, Op, Sp = calculate_peptide_values(peptide)
		Hp = Hs-N
		Beta = Hp*Y20 + Cp*Y13 + Np*Y15 + Op*Y17 + Sp*Y33
		
		V0 = calculate_V0_selection2(df, row, number_of_zeros)
		V1_yield = calculate_V1_selection2(df, row, number_of_T2)
		for index, V1 in enumerate(V1_yield):
			if V1 == 0:
				temp_k.append('')
			else:
				D2 = float(bwe_split[index])/100
				Y21 =D2/(1-D2)
				Theta = 1 + Beta + ((N-1)/2)*(Y21 + Y20)
				P =1 -  (1/((1/(1-V0))+ N*(Y21 - Y20)*Theta))
				try:
					k = (-1/t)*math.log(1-((V1-V0)/(P-V0)))	
				except ValueError:
					k = ''	
				finally:
					temp_k.append(k)
		final_data_df[peptide] = pd.Series(temp_k)
	return final_data_df

def calculate_V0_selection2(df, row, number_of_zeros):
	temp_V0 = []
	for i in range(number_of_zeros):
		#Position 0 =charge, position 1= mass, position 2=M0
		# M0 = float(row[i*6+3].strip())
		# M1 = float(row[i*6+4].strip())
		# M2 = float(row[i*6+5].strip())
		try:
			temp_V0.append((float(row[i*6+4].strip())+float(row[i*6+5].strip()))/(float(row[i*6+4].strip())+float(row[i*6+3].strip())+ float(row[i*6+5].strip())))
		except ZeroDivisionError:
			pass
		except ValueError:
			pass
		try:
			V0 = statistics.mean(temp_V0)
		except:
			V0 = 0
		return V0

def calculate_V1_selection2(df, row, number_of_T2):
	temp_peptide = row[number_of_T2*-6:]
	for i in range(number_of_T2):
		#M0 = float(temp_peptide[i*6].strip())
		#M1 = float(temp_peptide[i*6+1].strip())
		#M2 = float(temp_peptide[i*6+2].strip())
		try:
			V1_yield = (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6+2].strip()))/ (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6+2].strip())+float(temp_peptide[i*6].strip()))
		except ZeroDivisionError:
			V1_yield = 0
		except ValueError:
			V1_yield = 0
		finally:
			yield V1_yield

def calculate_FSR_selection_3(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2):
	import math
	final_data_df = pd.DataFrame()
	
	t = float(user_time_points.split(',')[-1])
	k_format = 'k({})'.format(t)
	temporary_list = [k_format for i in range(number_of_T2)]
	final_data_df['peptide'] = temporary_list
		
	X2 = 0.00015
	X1 = 1-X2
	Y20 = X2/X1
	Y13 = 0.011074/(1-0.011074)
	Y15 = (1-0.99635)/0.99635
	Y17 = 0.00037/0.99759
	Y33 = 0.0076/0.95
	Y18 = 0.00204/0.99759
	Y34 = 0.0422/0.95

	bwe_split = bwe.split(',')[-number_of_T2:]
	for peptide, row in df.iterrows():
		temp_k = []
		N = calculate_N(peptide, fsr_selection)
		Cp, Hs, Np, Op, Sp = calculate_peptide_values(peptide)
		Hp = Hs-N
		Gamma = ((Hp*(Hp-1)*(Y20**2) + Cp*(Cp-1)*(Y13**2) + Np*(Np-1)*(Y15**2) +Op*(Op-1)*(Y17**2) + Sp*(Sp-1)*(Y33**2))/2)+(Op*Y18+Sp*Y34+Hp*Y20*(Cp*Y13+Np*Y15+Op*Y17+Sp*Y33) + Cp*Y13*(Np*Y15+Op*Y17+Sp*Y33)+Np*Y15*(Op*Y17 +Sp*Y33) + Op*Y17*Sp*Y33)
		Beta = Hp*Y20 + Cp*Y13 + Np*Y15 + Op*Y17 + Sp*Y33
		V0 = calculate_V0_selection3(df, row, number_of_zeros)
		V1_yield = calculate_V1_selection3(df, row, number_of_T2)
		for index, V1 in enumerate(V1_yield):
			if V1 == 0:
				temp_k.append('')
			else:
				D2 = float(bwe_split[index])/100
				Y21 =D2/(1-D2)
				Theta = 1 + Beta + Gamma+ ((N-1)/2)*(Y21 + Y20)*(1+Beta) + ((N-1)/6)*(N-2)*(1+Beta)*((Y21**2)+Y21*Y20+(Y20**2))
				P =1 -  (1/((1/(1-V0))+ N*(Y21 - Y20)*Theta))
				try:
					k = (-1/t)*math.log(1-((V1-V0)/(P-V0)))	
				except ValueError:
					k = ''	
				finally:
					temp_k.append(k)
		final_data_df[peptide] = pd.Series(temp_k)
	return final_data_df

def calculate_V0_selection3(df, row, number_of_zeros):
	temp_V0 = []
	for i in range(number_of_zeros):
		#Position 0 =charge, position 1= mass, position 2=M0
		# M0 = float(row[i*6+3].strip())
		# M1 = float(row[i*6+4].strip())
		# M2 = float(row[i*6+5].strip())
		# M3 = float(row[i*6+6].strip())
		try:
			temp_V0.append((float(row[i*6+4].strip())+float(row[i*6+5].strip())+float(row[i*6+6].strip()))/(float(row[i*6+4].strip())+float(row[i*6+3].strip())+ float(row[i*6+5].strip())+float(row[i*6+6].strip())))
		except ZeroDivisionError:
			pass
		except ValueError:
			pass
		try:
			V0 = statistics.mean(temp_V0)
		except:
			V0 = 0
		return V0

def calculate_V1_selection3(df, row, number_of_T2):
	temp_peptide = row[number_of_T2*-6:]
	for i in range(number_of_T2):
		#M0 = float(temp_peptide[i*6].strip())
		#M1 = float(temp_peptide[i*6+1].strip())
		#M2 = float(temp_peptide[i*6+2].strip())
		#M3 = float(temp_peptide[i*6+3].strip())
		try:
			V1_yield = (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6+3].strip())+float(temp_peptide[i*6+2].strip()))/ (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6+3].strip())+float(temp_peptide[i*6+2].strip())+float(temp_peptide[i*6].strip()))
		except ZeroDivisionError:
			V1_yield = 0
		except ValueError:
			V1_yield = 0
		finally:
			yield V1_yield

def calculate_FSR_selection_4(folder_name, df, bwe, fsr_selection, user_time_points, number_of_zeros, number_of_T2):
	import math
	final_data_df = pd.DataFrame()
	
	t = float(user_time_points.split(',')[-1])
	k_format = 'k({})'.format(t)
	temporary_list = [k_format for i in range(number_of_T2)]
	final_data_df['peptide'] = temporary_list
		
	X2 = 0.00015
	X1 = 1-X2
	Y20 = X2/X1
	Y13 = 0.011074/(1-0.011074)
	Y15 = (1-0.99635)/0.99635
	Y17 = 0.00037/0.99759
	Y33 = 0.0076/0.95
	Y18 = 0.00204/0.99759
	Y34 = 0.0422/0.95

	bwe_split = bwe.split(',')[-number_of_T2:]
	for peptide, row in df.iterrows():
		temp_k = []
		N = calculate_N(peptide, fsr_selection)
		Cp, Hs, Np, Op, Sp = calculate_peptide_values(peptide)
		Hp = Hs-N
		Omega = ((Hp*(Hp-1)*(Hp-2)*(Y20**3) + Cp*(Cp-1)*(Cp-2)*(Y13**3) + Np*(Np-1)*(Np-2)*(Y15**3) +Op*(Op-1)*(Op-2)*(Y17**3) + Sp*(Sp-1)*(Sp-2)*(Y33**3))/6)+(((Hp*(Hp-1)*(Y20**2)*(Cp*Y13+Np*Y15+Op*Y17+Sp*Y33) + Cp*(Cp-1)*(Y13**2)*(Hp*Y20+Np*Y15+Op*Y17+Sp*Y33))+(Np*(Np-1)*(Y15**2)*(Hp*Y20+Cp*Y13+Op*Y17+Sp*Y33) +Op*(Op-1)*((Y17**2)+2*Y18)*(Hp*Y20+Cp*Y13+Np*Y15+Sp*Y33))+(Sp*(Sp-1)*((Y33**2)+2*Y34)*(Hp*Y20+Cp*Y13+Np*Y15+Op*Y17)))/2) +(Hp*Y20*Cp*Y13*(Np*Y15+Op*Y17+Sp*Y33)+Cp*Y13*Np*Y15*(Op*Y17+Sp*Y33)+Np*Y15*Op*Y17*Sp*Y33)
		Gamma = ((Hp*(Hp-1)*(Y20**2) + Cp*(Cp-1)*(Y13**2) + Np*(Np-1)*(Y15**2) +Op*(Op-1)*(Y17**2) + Sp*(Sp-1)*(Y33**2))/2)+(Op*Y18+Sp*Y34+Hp*Y20*(Cp*Y13+Np*Y15+Op*Y17+Sp*Y33) + Cp*Y13*(Np*Y15+Op*Y17+Sp*Y33)+Np*Y15*(Op*Y17 +Sp*Y33) + Op*Y17*Sp*Y33)
		Beta = Hp*Y20 + Cp*Y13 + Np*Y15 + Op*Y17 + Sp*Y33
		V0 = calculate_V0_selection4(df, row, number_of_zeros)
		V1_yield = calculate_V1_selection4(df, row, number_of_T2)
		for index, V1 in enumerate(V1_yield):
			if V1 == 0:
				temp_k.append('')
			else:
				D2 = float(bwe_split[index])/100
				Y21 =D2/(1-D2)
				Theta = 1 + Beta + Gamma + Omega + ((N-1)/2)*(Y21 + Y20)*(1+Beta+Omega) + ((N-1)/6)*(N-2)*(1+Beta)*(Y21**2)+Y21*Y20+(Y20**2)+((N-1)/24)*(N-2)*(N-3)*(Y21+Y20)*(Y21**2)+(Y20**2)
				P =1 -  (1/((1/(1-V0))+ N*(Y21 - Y20)*Theta))
				try:
					k = (-1/t)*math.log(1-((V1-V0)/(P-V0)))	
				except ValueError:
					k = ''	
				finally:
					temp_k.append(k)
		final_data_df[peptide] = pd.Series(temp_k)
	return final_data_df

def calculate_V0_selection4(df, row, number_of_zeros):
	temp_V0 = []
	for i in range(number_of_zeros):
		#Position 0 =charge, position 1= mass, position 2=M0
		# M0 = float(row[i*6+3].strip())
		# M1 = float(row[i*6+4].strip())
		# M2 = float(row[i*6+5].strip())
		# M3 = float(row[i*6+6].strip())
		# M4 = float(row[i*6+7].strip())
		try:
			temp_V0.append((float(row[i*6+4].strip())+float(row[i*6+5].strip())+float(row[i*6+7].strip())+float(row[i*6+6].strip()))/(float(row[i*6+4].strip())+float(row[i*6+3].strip())+float(row[i*6+7].strip())+ float(row[i*6+5].strip())+float(row[i*6+6].strip())))
		except ZeroDivisionError:
			pass
		except ValueError:
			pass
		try:
			V0 = statistics.mean(temp_V0)
		except:
			V0 = 0
		return V0

def calculate_V1_selection4(df, row, number_of_T2):
	temp_peptide = row[number_of_T2*-6:]
	for i in range(number_of_T2):
		#M0 = float(temp_peptide[i*6].strip())
		#M1 = float(temp_peptide[i*6+1].strip())
		#M2 = float(temp_peptide[i*6+2].strip())
		#M3 = float(temp_peptide[i*6+3].strip())
		#M4 = float(temp_peptide[i*6+4].strip())
		try:
			V1_yield = (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6+3].strip())+float(temp_peptide[i*6+4].strip())+float(temp_peptide[i*6+2].strip()))/ (float(temp_peptide[i*6+1].strip())+float(temp_peptide[i*6+4].strip())+float(temp_peptide[i*6+3].strip())+float(temp_peptide[i*6+2].strip())+float(temp_peptide[i*6].strip()))
		except ZeroDivisionError:
			V1_yield = 0
		except ValueError:
			V1_yield = 0
		finally:
			yield V1_yield

def calculate_peptide_values(peptide):
	AA_df = pd.read_csv('Amino_Acids_Comp.csv', index_col = 0)


	new_df = pd.DataFrame(columns = ['Cp','Hs','Np','Op','Sp'])
	
	for AA in peptide:
		try:
			new_df = new_df.append(AA_df.loc[AA])
		except KeyError:
			pass

	Cp = sum(new_df['Cp'])
	Hs = sum(new_df['Hs'])
	Np = sum(new_df['Np'])
	Op = sum(new_df['Op'])
	Sp = sum(new_df['Sp'])

	return Cp, Hs, Np, Op, Sp

def calculate_N(peptide, fsr_selection):
	AA_df = pd.read_csv('Amino_Acids_N.csv', index_col = 0)
	N_total = 0
	for AA in peptide:
		try:
			N_total += AA_df.loc[AA]['M' + str(fsr_selection)]
		except KeyError:
			pass
	return N_total

def create_columns(user_time_points):
	column_list = ['Peptides', 'Charge', 'SeqMass']
	for i in range(65, 65 + len(user_time_points.split(','))*6):
		column_list.append(chr(i))
	return column_list

def main():
	folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points = prompt()
	read_file_FSR(folder_name, fsr_selection, number_of_zeros, number_of_T2, bwe, user_time_points)

if __name__ == '__main__':
	main()
	print('Done')