import pymysql

con = pymysql.connect(host = "localhost", user = "django_app", password ="django_app123",
                      db = "django_app")
cur = con.cursor()

idol_id_sql = """UPDATE django_app.temp_chart SET idol_id = (SELECT idol.idol_id FROM idol WHERE temp_chart.idol_id = idol.idol_name)"""
cur.execute(idol_id_sql)
con.commit()

alter_temp_idol_sql = """ALTER TABLE django_app.temp_chart MODIFY idol_id int(11);"""
cur.execute(alter_temp_idol_sql)
con.commit()

insert_idol_sql = """INSERT INTO django_app.chart(chart_id, chart_music, chart_media, chart_portal, chart_total, chart_date, idol_id) 
                    SELECT chart_id, chart_music, chart_media, chart_portal, chart_total, chart_date, idol_id FROM django_app.temp_chart"""
cur.execute(insert_idol_sql)
con.commit()

con.close()