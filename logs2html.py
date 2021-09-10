import os
import sys


html_start = """
<!DOCTYPE html>
    <html lang = "en-US">
    <head>
        <meta charset = 'utf-8'>
        <meta http-equiv = "X-UA-Compatible" content = "IE=edge">
        <meta name = "viewport" content = "width=device-width,maximum-scale=2">
        <!-- Begin Jekyll SEO tag v2.5.0 -->
        <title> HPE Storage CI LOGS </title>
        <meta name = "generator" content = "Jekyll v3.8.5" />
        <meta property = "og:title" content = "HPE Storage CI LOGS" />
        <meta property = "og:locale" content = "en_US" />
        <link rel = "canonical" href = "https://hpe-storage.github.io/hpe_cinder_logs/" />
        <meta property = "og:url" content = "https://hpe-storage.github.io/hpe_cinder_logs/" />
        <meta property = "og:site_name" content = "HPE Storage CI LOGS" />
        <script type = "application/ld+json">
        {"@type": "WebSite", "headline": "HPE Storage CI LOGS", "url": "https://hpe-storage.github.io/hpe_cinder_logs/", "name": "HPE Storage CI LOGS", "@context": "http://schema.org"} </script>
        <!-- End Jekyll SEO tag -->
    </head>
    <body>
     <!-- HEADER -->
        <div id = "header_wrap" class = "outer">
           <header class = "inner">
              <h1 id = "project_title"> HPE Storage CI LOGS </h1>
              <h2 id = "project_tagline"> </h2>
            </header>
        </div>
        <!-- MAIN CONTENT -->
        <hr>
        <div id = "main_content_wrap" class = "outer">
            <style type = "text/css" media = "screen">
                .container {
                    margin: 0px auto
                    max-width: 80%
                    text-align: center
                 }
                h1 {
                    margin: 30px 0
                    font-size: 4em
                    line-height: 1
                    letter-spacing: -1px
                }
                table, td, th {
                    border: 0px solid black;
                }
            </style>
            <div class = "container"> """

html_end = """
            </div>
        </div>
        <!-- FOOTER  -->
        <hr>
        <div id="footer_wrap" class="outer">
            <footer class="inner">
                <p class="copyright">HPE Storage CI LOGS maintained by Storage team</p>
            </footer>
        </div>
    </body>
</html>
"""

ignore_ext = ['.xz', '.txt', '.log', '.gz', '.pdf', '.ini', '.json', '.conf', 'logs2html.py']


def create_html(path):
    table_data = ""
    # Ignore list
    if 'logs2html.py' in path:
        return
    # Remove symbolic links
    if os.path.islink(path):
        os.remove(path)
        return
    if os.path.isdir(path):
        cmd_list = os.listdir(path)
        if len(cmd_list) == 0 or path.split('/')[-1] == '.git':
            return
        table_start = "<table>\n"
        for i in cmd_list:
            new_path = os.path.join(path, i)
            # Ignore html files (these are only generated for folders)
            if os.path.islink(new_path):
                os.remove(new_path)
                continue
            if '.html' not in i:
                if os.path.isdir(new_path):
                    table_start = table_start + \
                        "<tr><td><a href = 'https://hpe-storage.github.io/hpe_cinder_logs/{}/{}.html'>{}</a></td></tr>\n".format(
                            new_path.split(sys.argv[1])[-1], i, i)
                    # Recurse for next folder
                    create_html(new_path)
                else:
                    # Change extension
                    if not any([x in new_path for x in ignore_ext]):
                        os.rename(new_path, new_path + '.txt')
                        i = i + '.txt'
                    table_start = table_start + \
                        "<tr><td><a href = 'https://hpe-storage.github.io/hpe_cinder_logs/{}'>{}</a></td></tr>\n".format(
                            new_path.split(sys.argv[1])[-1], i)

        table_data = table_start + "</table>\n"

    html_page = html_start + table_data + html_end
    if os.path.isdir(path):
        with open(os.path.join(path, (path.split('/')[-1] + '.html')), "w") as file:
            file.write(html_page)


create_html(sys.argv[1])

