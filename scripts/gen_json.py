#!/usr/bin/env python
# coding=utf-8

import os
import json
import sys


data_name = ''
root_dir = ''
data_dir = ''
files_dir = ''


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            yield file



def gen_json(paths):
    d = [{"imgSrc": path} for path in paths]
    with open(data_dir, "w+") as f:
        json.dump(d, f)


if __name__ == "__main__":
    data_name = ''
    if len(sys.argv) > 1:
        data_name = sys.argv[1]
    
    if data_name == '':
        raise ValueError("文件参数不能为空") 
    
    script_dir = os.path.dirname(os.path.abspath(__file__))

    root_dir = os.path.dirname(script_dir)
    
    files_dir = os.path.join(root_dir,  data_name)
    data_dir = os.path.join(root_dir,  "json", data_name + '.json')
    
    # print("文件路径:", files_dir)
    
    gen_json(file_name(files_dir))
    
   
    
   
        
        
        
    