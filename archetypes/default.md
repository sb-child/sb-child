+++
date = '{{ .Date }}'
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
comment_id = "{{ substr ( sha256 ( printf "%s %d %f" .File.ContentBaseName now.UnixNano math.Rand ) ) 0 32 }}"
draft = true
+++
