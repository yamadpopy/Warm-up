# -*- coding: utf-8 -*-
import os
import yaml

def yaml_save(path1,dic):
    os.makedirs(os.path.dirname(path1),exist_ok=True)
    with open(path1,'w',encoding='utf-8')as f:
        yaml.dump(
            dic,f,
            default_flow_style=False,
            allow_unicode=True,
            )