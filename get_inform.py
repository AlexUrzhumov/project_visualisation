#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import html
import json
habr_articles =  open('articles.txt', 'r')
index = 1
for article in habr_articles:
    response = requests.get(article)
    tree = html.fromstring(response.text)

    path_to_nicks = '//li/div[@class = "comment_body "]/div[@class]/span[@class = "comment-item__user-info"]/a[@class = "comment-item__username"]/text()'
    path_to_ids = '//li/div[@class = "comment_body "]/div/@rel'
    path_to_parents = '//li/span/@data-parent_id'
    path_to_ratings = '//li/div[@class = "comment_body "]/div/div/div/span[@title]/text()'
    nick_names = tree.xpath(path_to_nicks)
    ids = tree.xpath(path_to_ids)
    parent_ids = tree.xpath(path_to_parents)
    raitings = tree.xpath(path_to_ratings)

    i = 0
    all_comments = dict()
    for elem in ids:
        all_comments[elem] = (nick_names[i], raitings[i], parent_ids[i])
        i += 1
    for elem in all_comments:
        print (elem,' : ', all_comments[elem])


    i = 0
    nodes = list()
    links = list()
    nodes.append({"id" : "0", "rating" : 20, "name" : "Article"})
    for elem in all_comments:
        x = all_comments[elem][1]
        if x[0] == "–":
            x ="0"
        nodes.append({"id" : elem, "rating" : int(x), "name" : all_comments[elem][0]})
        links.append({"target" : elem, "source"  : all_comments[elem][2]})

    graph = {"nodes" : nodes, "links" : links}
    path = 'graph' + str(index) + '.json'
    with open(path, 'w') as output_file:
        json.dump(graph, output_file, sort_keys=False)
    index += 1