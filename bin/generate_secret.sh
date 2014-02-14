#!/usr/bin/env bash
openssl rand -base64 100 | sed ':a;N;$!ba;s/\n//g' | sed 's/==$//g'
