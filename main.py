import pyautogui
import pyperclip
import time
import random
import shutil
import webbrowser as wb
import re
import os
import subprocess
from datetime import datetime
from PIL import ImageGrab
from bs4 import BeautifulSoup
import requests
import urllib.parse
from PIL import Image
from io import BytesIO
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import uuid
import json
import glob
import pydirectinput
import string
from pywinauto import Application
import psycopg2
import cv2
import sqlite3 

# Tại đây khai báo để gọi API sửa dụng upload DB UAT
API_TOKEN = 'https://wapi.weallnet.com/api/TOKEN_AccessToken/GetClientAccessToken'
API_SAVE_PHOTOS = 'https://wapi.weallnet.com/api/Photo/Save'
API_SAVE_IMAGES = 'https://wapi.weallnet.com/api/PhotoImage/Save'

# ========================================================================================= /   
# Tại các hàm phần này sẽ hỗ trợ xóa User trong CMS + User tùy chỉnh 

# Các bảng cần dùng: UserProfileID + FeaturePermissions + FeatureGroupPermissions + BusinessRoles ( Của DB WAN_Data )

# Sau khi đã tắt bên ( DB WAN_Data ) tiếp tục edit với DB WAN_Authen tại bảng: ASPNetUsers ( Đánh dấu vào cột IsDeactive = True )

# Hàm xóa giá trị trong file txt, có giá trị là số theo hàng
def delete_data_in_file(file_path, line_to_delete):
    try:
        # Đọc dữ liệu từ file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Kiểm tra và xóa dòng cần xóa
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip() != line_to_delete:
                    file.write(line)

        print(f'Dữ liệu đã được xóa thành công từ file {file_path}.')
    except Exception as e:
        print(f'Lỗi khi xóa dữ liệu từ file {file_path}: {e}')
        
# Kết nối với DB | Kiểm tra Data sử dụng trước khi chạy chương trình
def connectDB():
    
    try:
        conn = psycopg2.connect(
            
                # Data PROD
                host="172.16.33.100",
                port="5432",
                database="WAN_Data",
                user="wan_data",
                password="fbpSk9MPmjheVzEtR8Ax6Q4NWYa3JnqG"
                
                # # Data dev
                # host="172.16.34.100",
                # port="5432",
                # database="WAN_Data_DEV",
                # user="wan_data",
                # password="k24KC7VyqD4byG9MEKehVZQd"
        
                # # Data uat
                # host="172.16.34.100",
                # port="5432",
                # database="WAN_Data_UAT",
                # user="wan_data",
                # password="k24KC7VyqD4byG9MEKehVZQd"
                
                # Data wan_notifydata
                # host="172.16.33.100",
                # port="5432",
                # database="WAN_NotifyData",
                # user="wan_notifydata",
                # password="pdtKnFfCMwLysmJqhQu9WUxSv57zN3Pk"
                
 
                # ========================================= /
                
            )
        print("Connected to the database successfully!")
        return(conn)
    
    except psycopg2.Error as e:
        print(f"Unable to connect to the database. Error: {e}")
        return None

def connectDB_Authen():
    
    try:
        conn = psycopg2.connect(
            
              
                # ========================================= /
                
                #Database: Wan_authen
                host="172.16.33.100",
                port="5432",
                database="WAN_Authen",
                user="wan_authen",
                password="q5YcN4we9uhHt3AQkdaWp7zmTy2URPvf"
                
            )
        print("Connected to the database successfully!")
        return(conn)
    
    except psycopg2.Error as e:
        print(f"Unable to connect to the database. Error: {e}")
        return None

# Các hàm hộ trợ xóa user ra khỏi hệ thống + CMS
def Delete_userProfileID(userProfileID):
    userProfileID = int(userProfileID)

    # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB()
    cur = connection.cursor()

    # Thực hiện lệnh SQL để xóa dòng có "Id" tương ứng trong bảng "AspNetUsers"
    cur.execute('DELETE FROM "UserProfiles" WHERE "UserProfileID" = %s', (userProfileID,))

    # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
    connection.commit()
    cur.close()
    connection.close()

def Delete_ASPNetUsers(ID_Input):
    ID_Input = str(ID_Input)

    # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB_Authen()
    cur = connection.cursor()

    # Thực hiện lệnh SQL để xóa dòng có "Id" tương ứng trong bảng "AspNetUsers"
    cur.execute('DELETE FROM "AspNetUsers" WHERE "Id" = %s', (ID_Input,))

    # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
    connection.commit()
    cur.close()
    connection.close()
    
# Lọc ra tên của Userprofile đang được đang bài trên Weallnet
def select_FullName_From_UserProfilesID(UserProfilesID):
    
    UserProfilesID = str(UserProfilesID)

    cur = connectDB().cursor()

    # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên


    cur.execute('SELECT "FullName" FROM "UserProfiles" WHERE "UserProfileID" = %s', (UserProfilesID,))


    rows = cur.fetchall()
    
    for row in rows:
        
        return(row[0])


    # Ngắt kết nối khi lấy dữ liệu xong

    cur.close()
    connectDB().close()
    
# Lọc ra Rule của User của bảng FeaturePermissions
def select_BusinessRoleID_From_FeaturePermissions(UserProfilesID):
    
    UserProfilesID = str(UserProfilesID)

    cur = connectDB().cursor()

    # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên


    cur.execute('SELECT "BusinessRoleID" FROM "FeaturePermissions" WHERE "UserProfileID" = %s', (UserProfilesID,))


    rows = cur.fetchall()
    
    for row in rows:
        
        return(row[0])


    # Ngắt kết nối khi lấy dữ liệu xong

    cur.close()
    connectDB().close()
    
# Lọc ra Rule của User của bảng FeatureGroupPermissions
def select_BusinessRoleID_From_FeatureGroupPermissions(UserProfilesID):
    
    UserProfilesID = str(UserProfilesID)

    cur = connectDB().cursor()

    # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên


    cur.execute('SELECT "BusinessRoleID" FROM "FeatureGroupPermissions" WHERE "UserProfileID" = %s', (UserProfilesID,))


    rows = cur.fetchall()
    
    for row in rows:
        
        return(row[0])


    # Ngắt kết nối khi lấy dữ liệu xong

    cur.close()
    connectDB().close()

# Get ID user dạng Code trong bảng UserProfiles
def select_UserId_From_UserProfiles(UserProfilesID):
    
    UserProfilesID = str(UserProfilesID)

    cur = connectDB().cursor()

    # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên


    cur.execute('SELECT "UserId" FROM "UserProfiles" WHERE "UserProfileID" = %s', (UserProfilesID,))


    rows = cur.fetchall()
    
    for row in rows:
        
        return(row[0])


    # Ngắt kết nối khi lấy dữ liệu xong

    cur.close()
    connectDB().close()

# Update vào Enable bảng FeatureGroupPermissions
def Update_Enable_FeatureGroupPermissions(userProfileID):
    
    userProfileID =  str(userProfileID)

    # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB()
    cur = connection.cursor()

    # Thực hiện lệnh SQL để cập nhật cột "Code"
    cur.execute('UPDATE "FeatureGroupPermissions" SET "Enabled" = %s, "Active" = %s WHERE "UserProfileID" = %s', ('False', 'False', userProfileID))

    # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
    connection.commit()
    cur.close()
    connection.close()

# Update vào Enable bảng FeaturePermissions
def Update_Enable_FeaturePermissions(userProfileID):
    
    userProfileID =  str(userProfileID)

    # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB()
    cur = connection.cursor()

    # Thực hiện lệnh SQL để cập nhật cột "Code"
    cur.execute('UPDATE "FeaturePermissions" SET "Enabled" = %s WHERE "UserProfileID" = %s', ('False', userProfileID))

    # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
    connection.commit()
    cur.close()
    connection.close()
   
# Update vào Enable bảng UserProfiles
def Update_IsRemove_UserProfiles(userProfileID):
    
    userProfileID =  str(userProfileID)

    # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB()
    cur = connection.cursor()

    # Thực hiện lệnh SQL để cập nhật cột "Code"
    cur.execute('UPDATE "UserProfiles" SET "IsRemove" = %s WHERE "UserProfileID" = %s', ('True', userProfileID))

    # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
    connection.commit()
    cur.close()
    connection.close()
  
# Update vào IsDeactive bảng AspNetUsers Authen DB
def Update_IsDeactive_ASPNetUsers(userProfileID):
    
    userProfileID =  str(userProfileID)

    # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB_Authen()
    cur = connection.cursor()

    # Thực hiện lệnh SQL để cập nhật cột "Code"
    cur.execute('UPDATE "AspNetUsers" SET "IsDeactive" = %s WHERE "Id" = %s', ('TRUE', userProfileID))

    # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
    connection.commit()
    cur.close()
    connection.close()

# Triển khai chạy các hàm trên
def run_Remove_User_CMS_By_ID():
    
    # Lọc Thông tin
    # print(select_FullName_From_UserProfilesID(item))
    # print(select_BusinessRoleID_From_FeatureGroupPermissions(item))
    # print(select_BusinessRoleID_From_FeaturePermissions(item))
    
    # ======================================== /
    
    list_UserID = read_File_Txt_On_Line_Value('list_User_Creator.txt')

    for item_Update in list_UserID: 
        
        print(item_Update)
        
        # Bắt đầu cập nhật các trường để block user này.
        Update_IsDeactive_ASPNetUsers((select_UserId_From_UserProfiles(item_Update)))
        Update_Enable_FeatureGroupPermissions(item_Update)
        Update_Enable_FeaturePermissions(item_Update)
        Update_IsRemove_UserProfiles(item_Update)
        #Delete_userProfileID(item_Update)
        delete_data_in_file('list_User_Creator.txt', item_Update)

# ========================================================================================= /   
# Hàm giúp lấy ra giá trị theo hàng trong file txt lưu vào biến
def read_File_Txt_On_Line_Value(file_Path):
    
    data_Save = []
    file_Path = str(file_Path)
    
    # Mở file txt để đọc
    with open(file_Path, 'r', encoding='utf-8') as file:
        # Đọc từng dòng và xử lý
        for line in file:
            # In giá trị của từng dòng
            data_Save.append((line.strip()))  # strip() để loại bỏ ký tự xuống dòng và khoảng trắng thừa
            
    return(data_Save)
            
# Xóa bắt đầu và kết thúc bằng "[" và "]" trong string
def remove_brackets_from_string(input_string):
    # Kiểm tra nếu chuỗi bắt đầu và kết thúc bằng "[" và "]" hoặc chỉ có dấu "["
    if (input_string.startswith("[") and input_string.endswith("]")):
        # Sử dụng slicing để loại bỏ "[" và "]"
        modified_string = input_string[1:-1]
    else:
        # Nếu không bắt đầu và kết thúc bằng "[" và "]" hoặc không có "[", giữ nguyên chuỗi
        modified_string = input_string

    return modified_string

# Xóa bắt đầu và kết thúc bằng ' và ' trong string
def remove_brackets_from_string_2(input_string):
    # Kiểm tra nếu chuỗi bắt đầu và kết thúc bằng "[" và "]" hoặc chỉ có dấu "["
    if (input_string.startswith("'") and input_string.endswith("'")) or (input_string.count("'") == 1 ):
        # Sử dụng slicing để loại bỏ "[" và "]"
        modified_string = input_string[1:-1]
    else:
        # Nếu không bắt đầu và kết thúc bằng "[" và "]" hoặc không có "[", giữ nguyên chuỗi
        modified_string = input_string
    
    #
    text = modified_string.lstrip("'")
    return text

# Khai báo Token, để có thể truy cập lên DB
def getToken():
    
    try :
        r = requests.post(API_TOKEN,
                        
            # # UAT => Test      
            # json={
            #     "clientId": "WANBMS",
            #     "clientSecret": "QVFOGGL5ECOTJE3RZPVRR455IWAN01",
            #     "scope": "WANAPI"
            #     }
            
            # PROD
            json={
                "clientId": "WANBMS",
                "clientSecret": "QVFOGGL5ECOTJE3RZPVRR455IWAN01",
                "scope": "WANAPI"
                }
            
            
            )

        
        return r.json().get('access_token')
    except requests.exceptions.HTTPError as err: print(f"Http Error: {err}")

TOKEN = getToken()

# Hàm ghi giá trị txt vào file 
def write_Value_To_File_Txt(file_path, values_to_append):

    values_to_append = str(values_to_append)
    # File path to append the values
        
    with open(file_path, 'a', encoding='utf-8') as file:
        file.writelines(values_to_append + "\n")
        
# Hàm tính kích thước của Hình
def get_image_dimensions_from_url(image_url):
    
    try:
        # Tải hình ảnh từ URL
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Đọc hình ảnh từ dữ liệu nhận được
        image = Image.open(BytesIO(response.content))
        
        # Lấy thông tin chiều cao và chiều rộng của hình ảnh
        width, height = image.size
        
        return width, height
    
    except Exception as e:
        print("Error:", str(e))
        return None, None

# Cập nhật chiều Cao x Dài cho Videos
def update_Hight_Width_Video():
    
     # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB()
    cur = connection.cursor()
    # Các bước sẽ thực hiện 
        # Bước 1: Lấy ID video theo vòng lặp từ lớn đến nhỏ, có khung Weight trống
        # Bước 2: Lưu đè giá trị vào file txt
        # Bước 3: Tiến hành vòng lặp để lấy VideoScreenShot có trong DB, để xác định kích thước
    
    # --------------------------------------- /

    # Hàm lấy width, height của video
    def get_video_dimensions(video_url):
        
        try:
            cap = cv2.VideoCapture(video_url)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return width, height

        except Exception as e: print("Error:", e)
        
        return None, None

    # Hàm lấy các ID video từ DB
    def get_Information_VideoID_New():
        
            Data_Save = [[],[],[]]

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            
            cur.execute( 'SELECT "VideoID", "RawPlayURL" FROM "Videos" WHERE "Height" IS NULL ORDER BY "VideoID" DESC LIMIT 1' )

            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: 
                
                Data_Save[0].append(row[0])
                
                # Lấy width, height của video
                height, width = get_video_dimensions(row[1])
                Data_Save[1].append(height)
                Data_Save[2].append(width)
                
            return Data_Save
    
    # Hàm update lại Code random cho DB Photos
    def Update_Code_Random_DB(Height ,Width, VideoID):
        
        if int(Height) > int(Width): IsVertical = True
        else: IsVertical = False
        Width = int(Width)
        Height = int(Height)
        VideoID = int(VideoID)
        
        cur = connection.cursor()

        # Thực hiện lệnh SQL để cập nhật cột "Code"
    
        cur.execute('UPDATE "Videos" SET "Height" = %s, "Width" = %s , "IsVertical" = %s Where "VideoID" = %s ', (int(Height), int(Width), IsVertical, VideoID))


        # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
        connection.commit()

    
    # Chạy test
    
    data_Update_DB = get_Information_VideoID_New()
    print(data_Update_DB)
    # Update_Code_Random_DB(data_Update_DB[2][0], data_Update_DB[1][0], data_Update_DB[0][0])
    # print('/-- Update for VideoID: ', data_Update_DB[0][0], ' --/')
        
    # Ngắt kết nối khi lấy dữ liệu xong
    
    
    cur.close()
    connectDB().close()

# Cập nhật chiều Cao x Dài cho Movies
def update_Hight_Width_Movies():
    
     # Tạo kết nối đến cơ sở dữ liệu
    connection = connectDB()
    cur = connection.cursor()
    # Các bước sẽ thực hiện 
        # Bước 1: Lấy ID video theo vòng lặp từ lớn đến nhỏ, có khung Weight trống
        # Bước 2: Lưu đè giá trị vào file txt
        # Bước 3: Tiến hành vòng lặp để lấy VideoScreenShot có trong DB, để xác định kích thước
    
    # --------------------------------------- /

    # Hàm lấy width, height của video
    def get_video_dimensions(video_url):
        
        try:
            cap = cv2.VideoCapture(video_url)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return width, height

        except Exception as e: print("Error:", e)
        
        return None, None

    # Hàm lấy các ID video từ DB
    def get_Information_MovieID_New():
        
            Data_Save = [[],[],[]]

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            
            cur.execute( 'SELECT "MovieID", "RawPlayURL" FROM "Movies" WHERE "Height" IS NULL ORDER BY "MovieID" DESC LIMIT 1' )

            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: 
                
                Data_Save[0].append(row[0])
                
                # Lấy width, height của video
                height, width = get_video_dimensions(row[1])
                Data_Save[1].append(height)
                Data_Save[2].append(width)
                
            return Data_Save
    
    # Hàm update lại Code random cho DB Photos
    def Update_Code_Random_DB(Height ,Width, VideoID):
        
        if int(Height) > int(Width): IsVertical = True
        else: IsVertical = False
        Width = int(Width)
        Height = int(Height)
        VideoID = int(VideoID)
        
        cur = connection.cursor()

        # Thực hiện lệnh SQL để cập nhật cột "Code"
    
        cur.execute('UPDATE "Movies" SET "Height" = %s, "Width" = %s , "IsVertical" = %s Where "MovieID" = %s ', (int(Height), int(Width), IsVertical, VideoID))


        # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
        connection.commit()

    
    # Chạy 
    for i in range(1000):
        data_Update_DB = get_Information_MovieID_New()
        Update_Code_Random_DB(data_Update_DB[2][0], data_Update_DB[1][0], data_Update_DB[0][0])
        print('/-- Update for MovieID: ', data_Update_DB[0][0], ' --/')
            
    # Ngắt kết nối khi lấy dữ liệu xong
    
    cur.close()
    connectDB().close()

# Hàm xóa hình photo trong DB ------------------------------------/
def remove_Photo_DB(ChannelConfigID_Use):
    
    # Hàm lấy các ID video từ DB
    def get_Information_Photo(ChannelConfigID):
        
            Data_Save = []
            
            ChannelConfigID = int(ChannelConfigID)

            cur = connectDB().cursor()

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            cur.execute('SELECT "PhotoID" FROM "Photos" WHERE "ChannelConfigID" = %s ORDER BY "PhotoID" DESC', (ChannelConfigID,))
            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: Data_Save.append(row[0])
            
            # Ngắt kết nối khi lấy dữ liệu xong
            cur.close()
            connectDB().close()
            
            return Data_Save
    
    def remove_PhotoID(channel_Config):
        # Establish the database connection
        conn = connectDB()  # Replace with your actual connection code
        cur = conn.cursor()

        try:
            # Use parameterized query to avoid SQL injection
            cur.execute('DELETE FROM "Photos" WHERE "ChannelConfigID" = %s', (channel_Config,))

            # Commit the transaction
            conn.commit()
        except Exception as e:
            # Handle any exceptions that might occur
            print("Error:", e)
            conn.rollback()  # Roll back changes if an error occurs
        finally:
            # Close the cursor and connection
            cur.close()
            conn.close()
        
    def remove_PhotoImages(photo_id):
        # Establish the database connection
        conn = connectDB()  # Replace with your actual connection code
        cur = conn.cursor()

        try:
            # Use parameterized query to avoid SQL injection
            cur.execute('DELETE FROM "PhotoImages" WHERE "PhotoID" = %s', (photo_id,))

            # Commit the transaction
            conn.commit()
        except Exception as e:
            # Handle any exceptions that might occur
            print("Error:", e)
            conn.rollback()  # Roll back changes if an error occurs
        finally:
            # Close the cursor and connection
            cur.close()
            conn.close()
            
    # Nhập ID ChannelConfigID cần xóa
    PhotoID_List = get_Information_Photo(ChannelConfigID_Use)
    
    for item in PhotoID_List:
        print('/--- Remove PhotoID: ', item, ' ---/')
        remove_PhotoImages(item)
        
    remove_PhotoID(ChannelConfigID_Use)

# # Hàm hỗ trợ chỉnh sửa lại title + name + mô tả bài viết
def update_Name_Title_Video():

    # Hàm lấy các ID video từ DB
    def get_Information_VideoID_New():
        
            Data_Save = [[],[],[]]

            cur = connectDB().cursor()

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            
            cur.execute( 'SELECT "VideoID", "Description" FROM "Videos" WHERE "Name" LIKE \'%[%\' ORDER BY "VideoID" DESC LIMIT 600' )

            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: 
                
                Data_Save[0].append(row[0]) # ID Video
                Data_Save[1].append(row[1]) # Decription


            # Ngắt kết nối khi lấy dữ liệu xong

            cur.close()
            connectDB().close()
            
            return Data_Save
    
    # Hàm update lại Code random cho DB Photos
    def Update_Code_Random_DB(Name_Video ,Title_Video, Description_Video, VideoID):
        
        Name_Video = Name_Video[:200]
        Title_Video = Title_Video[:200]


        VideoID = int(VideoID)
        # Tạo kết nối đến cơ sở dữ liệu
        connection = connectDB()
        cur = connection.cursor()

        # Thực hiện lệnh SQL để cập nhật cột "Code"
    
        cur.execute('UPDATE "Videos" SET "Name" = %s, "Title" = %s , "Description" = %s Where "VideoID" = %s ', (str(Name_Video), str(Title_Video), str(Description_Video), VideoID))


        # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
        connection.commit()
        cur.close()
        connection.close()
    
    #
    data_Use = get_Information_VideoID_New()
    
    for item in range(len(data_Use[0])):
        
        title_Need_Fix = data_Use[1][item]
        ID_Video_Need_Fix = data_Use[0][item]
        
        clear_Item = remove_brackets_from_string_2(remove_brackets_from_string(title_Need_Fix))
        if len(clear_Item) < 1: 
            print("Bài viết không có tiều đề .......................................")
            Update_Code_Random_DB('...' ,'...', '...', ID_Video_Need_Fix)
        else: 
            print(clear_Item)
            Update_Code_Random_DB(clear_Item ,clear_Item, clear_Item, ID_Video_Need_Fix)

# Hàm giúp tắt các Video không có title
def turn_Off_Video_No_have_Title():
    
    # Hàm lấy các ID video từ DB
    def get_Information_Video():
        
            Data_Save = []

            cur = connectDB().cursor()

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            cur.execute('SELECT "VideoID" FROM "Videos" WHERE "Name" = %s ORDER BY "VideoID" DESC', ('...',))
            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: Data_Save.append(row[0])
            
            # Ngắt kết nối khi lấy dữ liệu xong
            cur.close()
            connectDB().close()
            
            return Data_Save
        
    # Chạy update để turn off video đó
    def Update_Enable_Video_DB(VideoID):
        
      
        VideoID = int(VideoID)
        # Tạo kết nối đến cơ sở dữ liệu
        connection = connectDB()
        cur = connection.cursor()

        # Thực hiện lệnh SQL để cập nhật cột "Code"
    
        cur.execute('UPDATE "Videos" SET "ReferenceSource" = %s Where "VideoID" = %s ', ('Fixed', VideoID))


        # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
        connection.commit()
        cur.close()
        connection.close()
    
    # Chạy hàm chính 
    for item in get_Information_Video(): 
        
        print(item)
        
        Update_Enable_Video_DB(item)

# Hàm Update Category cho bảng News
def update_Id_AND_Name_Category_For_News_Table():
    
    cur = connectDB().cursor()
    
    connection_Update = connectDB()
    cur_Update = connection_Update.cursor()

    # Hàm lấy các ID video từ DB
    def get_Information_News():
        
            Data_Save = []

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            
            cur.execute( 'SELECT "NewsID" FROM "Newss" Where "Category" IS NULL OR "CategorysName" IS NULL  ORDER BY "NewsID" DESC LIMIT 10000' )

            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: 
                
                Data_Save.append(row[0]) # NewsID
            
            return Data_Save
    
    # Sau khi có được danh sách ID tiếp tục tìm catergoty ID bên bảng NewsCategoryLinks
    def get_Information_NewsCategoryLinks(News_ID):
        
        try :

            News_ID = int(News_ID)
            
            Data_Save = []

            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            cur.execute( 'SELECT "NewsCategoryID" FROM "NewsCategoryLinks" WHERE "NewsID" = %s ' , (News_ID,))
            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: 
                
                Data_Save.append(row[0]) # NewsID
            
            return Data_Save[0]
        
        except: return ""
    
    # Get NewCategories Name
    def get_Information_NewCategories_Name(NewCategories_ID):
        
        try :

            NewCategories_ID = int(NewCategories_ID)
            
            Data_Save = []
       
            # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
            cur.execute( 'SELECT "Name" FROM "NewsCategories" WHERE "NewsCategoryID" = %s ' , (NewCategories_ID,))
            rows = cur.fetchall()

            # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
            for row in rows: 
                
                Data_Save.append(row[0]) # NewsID
            
            return Data_Save[0]
        
        except: return ""
    
    # Update vào lại bảng Newss
    def Update_Enable_News_DB(News_ID, Category_ID, Category_Name):
        
         # Tạo kết nối đến cơ sở dữ liệu
        try :

            News_ID = int(News_ID)
            Category_ID = int(Category_ID)
            Category_Name = str(Category_Name)
       
            # Thực hiện lệnh SQL để cập nhật cột "Code"
        
            cur_Update.execute('UPDATE "Newss" SET "Category" = %s, "CategorysName" = %s Where "NewsID" = %s ', (Category_ID, Category_Name, News_ID))

            # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
            connection_Update.commit()
 
        except: return ""

    # Chạy chương trình -------------------- /
    data_News_Table = get_Information_News()

    for NewsID_Item in data_News_Table:
        
        print(NewsID_Item)
    
        Category_ID_Get = get_Information_NewsCategoryLinks(NewsID_Item)
        
        Category_Name_Get = get_Information_NewCategories_Name(Category_ID_Get)
        
        print("Update News ID: " + str(NewsID_Item) + ", Có Name Category: " + str(Category_Name_Get) +  ", Có ID Category: " + str(Category_ID_Get) )
        
        Update_Enable_News_DB(NewsID_Item, Category_ID_Get, Category_Name_Get)
        
    # Ngắt kết nối khi lấy dữ liệu xong
    cur.close()
    connectDB().close()

# Hàm xóa photo không có hình bên Photoimages
def optimize_Photo_Table():
    
    cur = connectDB().cursor()

    
    # Hàm lấy các ID video từ DB
    def get_Information_VideoID_New():
        
        data_Save = []

        cur = connectDB().cursor()

        # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên
        
        cur.execute( 'SELECT "PhotoID" FROM "Photos" ORDER BY "PhotoID" ' )

        rows = cur.fetchall()

        # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
        for row in rows: 
            data_Save.append(row[0])
        

        # Ngắt kết nối khi lấy dữ liệu xong

        cur.close()
        connectDB().close()
        
        return data_Save

    # Các hàm hộ trợ xóa user ra khỏi hệ thống + CMS
    def Delete_userProfileID(PhotoID_Input):
        PhotoID_Input = int(PhotoID_Input)

        # Tạo kết nối đến cơ sở dữ liệu
        connection = connectDB()
        cur = connection.cursor()

        # Thực hiện lệnh SQL để xóa dòng có "Id" tương ứng trong bảng "AspNetUsers"

        cur.execute('DELETE FROM "Photos" WHERE "PhotoID" = %s', (PhotoID_Input,))


        # Commit thay đổi vào cơ sở dữ liệu và đóng kết nối
        connection.commit()

    # Hàm kiểm tra photoID có trong bảng Photoimages hay không
    def check_Photo_ID_Have_In_PhotoImages(PhotoImageID_Input):
        
        PhotoImageID_Input = int(PhotoImageID_Input)
        
        data_Save = []

        # Hàm hỗ trợ lấy dữ liệu ChannelConfigID + ID video tiktok + thời gian tải lên

        cur.execute('SELECT "PhotoImageID" FROM "PhotoImages" WHERE "PhotoID" = %s', (PhotoImageID_Input,))
        rows = cur.fetchall()


        # Lưu vào Data => Chuẩn bị tới bước tiếp theo phân loại và xóa trash
        for row in rows: 
            data_Save.append(row[0])
            
            break
        
       
        return len(data_Save)
        
    for photoID in get_Information_VideoID_New():
        
        print(photoID)
        
        if check_Photo_ID_Have_In_PhotoImages(photoID) == 0 :
            
            print("Xoa PhotoID nay")
            
            Delete_userProfileID(photoID)
            

    # Ngắt kết nối:
    cur.close()
    connectDB().close()

# Hàm lấy tên bảng dựa vào tên cột, để sử dụng Tool API
def get_Table_Name_by_Column(column_name):
    column_name = str(column_name)
    
    try:
        # Kết nối đến cơ sở dữ liệu
        conn = connectDB()
        cur = conn.cursor()

        # Lấy thông tin về tên bảng có chứa cột
        cur.execute(f"SELECT table_name FROM information_schema.columns WHERE column_name = '{column_name}'")
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Đóng kết nối
        cur.close()
        conn.close()
         
# Triển khai các chương trình ===============================/
# turn_Off_Video_No_have_Title()
# remove_Photo_DB(1310)
# get_Name_Column_Table('PhotoImages')
# get_Name_Column_Table('Photos')
# update_Category_For_News_Table()
# run_Remove_User_CMS_By_ID()
# update_Id_AND_Name_Category_For_News_Table()
# Hòa : NotifyMessage
# Hàm hỗ trợ lấy tên bảng dựa vào tên cột
# print(get_Table_Name_by_Column('totalNotify'))
# update_Hight_Width_Movies()
update_Id_AND_Name_Category_For_News_Table()