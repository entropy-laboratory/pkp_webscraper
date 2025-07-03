def build_html_email(cheap_connections):
    html_body = f"""
    <html>
    <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f9f9f9;
            padding: 20px;
            color: #333;
        }}
        .date-section {{
            background-color: #ffffff;
            border-left: 4px solid #4CAF50;
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .date-section h2 {{
            margin-top: 0;
        }}
        .connection {{
            margin-left: 15px;
            margin-bottom: 10px;
        }}
        .links {{
            margin-top: 10px;
            font-size: 0.95em;
            color: #555;
        }}
        </style>
    </head>
    <body>
        <h1>📢 Tanie połączenia na nadchodzące soboty</h1>
    """

    for block in cheap_connections:
        lines = block.strip().split("\n")
        data = lines[0].replace("🗓️", "").strip()
        connections = "\n".join(f"<div class='connection'>{line}</div>" for line in lines[1:-2])
        url_lines = lines[-2:]
        links = "<br>".join(url_lines).replace("➡️", "➡️ Wyjazd:").replace("⬅️", "⬅️ Powrót:")

        html_body += f"""
        <div class="date-section">
        <h2>🗓️ {data}</h2>
        {connections}
        <div class="links">
            {links}
        </div>
        </div>
        """

    html_body += """
    </body>
    </html>
    """
    return html_body
