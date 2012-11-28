#!/bin/sh

query=""

for this_query_term in $@
do
  query="${query}${this_query_term}+"
done

url="http://www.google.com/search?q=${query}"

remote_addr=`who am i | awk -F\( '{print $2}' | sed 's/)//'`

if [ -z "$remote_addr" ]; then
  elinks "$url"
else
  links "$url"
fi
