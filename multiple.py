"""Shaked's classroom multiplication app, version 4.1.

Run: streamlit run multiple.py
Production: set SHAKED_DATABASE_URL in Streamlit Secrets to a dedicated PostgreSQL database.
Local test only: set SHAKED_DEV_DB to a writable SQLite file path.
All grading, accounts, PIN hashes, progress and averages are managed by the server.
The complete 200-question bank and responsive frontend are embedded in this file.
"""
"""A fixed, numbered bank: 80 beginner, 60 intermediate, 60 advanced stories."""

STORY_TEMPLATES = [
    # Level A: one clearly stated collection of equal groups.
    (0, "יֵשׁ {a} שַׂקִּיּוֹת. בְּכָל שַׂקִּית {b} תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "עַל הַשֻּׁלְחָן {a} צַלָּחוֹת. בְּכָל צַלַּחַת {b} עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "בַּגִּנָּה {a} שׁוּרוֹת. בְּכָל שׁוּרָה {b} פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?"),
    (0, "יֵשׁ {a} קֻפְסָאוֹת. בְּכָל קֻפְסָה {b} עֶפְרוֹנוֹת. כַּמָּה עֶפְרוֹנוֹת יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "יֵשׁ {a} יְלָדִים. כָּל יֶלֶד מְקַבֵּל {b} בָּלוֹנִים. כַּמָּה בָּלוֹנִים צָרִיךְ לְכֻלָּם?"),
    (0, "בַּסַּל {a} חֲבִילוֹת. בְּכָל חֲבִילָה {b} לַחְמָנִיּוֹת. כַּמָּה לַחְמָנִיּוֹת יֵשׁ בַּסַּל?"),
    (0, "יֵשׁ {a} דַּפִּים. עַל כָּל דַּף {b} מַדְבֵּקוֹת. כַּמָּה מַדְבֵּקוֹת יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "יֵשׁ {a} סַלִּים. בְּכָל סַל {b} כַּדּוּרִים. כַּמָּה כַּדּוּרִים יֵשׁ בְּכָל הַסַּלִּים יַחַד?"),
    (0, "בַּסִּפְרִיָּה {a} מַדָּפִים. עַל כָּל מַדָּף {b} סְפָרִים. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?"),
    (0, "בַּיַּעַר {a} עֵצִים. עַל כָּל עֵץ {b} צִפּוֹרִים. כַּמָּה צִפּוֹרִים יֵשׁ עַל הָעֵצִים?"),
    (0, "יֵשׁ {a} שֻׁלְחָנוֹת. לְיַד כָּל שֻׁלְחָן {b} כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "יֵשׁ {a} צְמִידִים. בְּכָל צָמִיד {b} חָרוּזִים. כַּמָּה חָרוּזִים יֵשׁ בְּכָל הַצְּמִידִים?"),
    (0, "יֵשׁ {a} קַרְטוֹנִים. בְּכָל קַרְטוֹן {b} בַּקְבּוּקִים. כַּמָּה בַּקְבּוּקִים יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "בַּמִּשְׂחָק {a} מִגְדָּלִים. בְּכָל מִגְדָּל {b} קֻבִּיּוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ בְּסַךְ הַכֹּל?"),
    (0, "יֵשׁ {a} זֵרִים. בְּכָל זֵר {b} פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בְּכָל הַזֵּרִים?"),
    (0, "יֵשׁ {a} אֲרִיזוֹת. בְּכָל אֲרִיזָה {b} קְלָפִים. כַּמָּה קְלָפִים יֵשׁ בְּסַךְ הַכֹּל?"),
    # Level B: varied multiplication facts, all factors at most ten.
    (1, "לַהַצָּגָה הֵכִינוּ {a} שׁוּרוֹת שֶׁל כִּסְאוֹת, וּבְכָל שׁוּרָה {b} כִּסְאוֹת. כַּמָּה אֲנָשִׁים יוּכְלוּ לָשֶׁבֶת?"),
    (1, "בְּכָל עַמּוּד בָּאַלְבּוֹם יֵשׁ מָקוֹם לְ־{b} תְּמוּנוֹת. מִלְּאוּ {a} עַמּוּדִים. כַּמָּה תְּמוּנוֹת הִכְנִיסוּ?"),
    (1, "בְּמֶשֶׁךְ {a} יָמִים קָרְאוּ בְּכָל יוֹם {b} עַמּוּדִים. כַּמָּה עַמּוּדִים קָרְאוּ בְּכָל הַיָּמִים יַחַד?"),
    (1, "לְכָל קְבוּצָה מְחַלְּקִים {b} כַּרְטִיסִים. בַּכִּתָּה יֵשׁ {a} קְבוּצוֹת. כַּמָּה כַּרְטִיסִים צָרִיךְ לְחַלֵּק?"),
    (1, "בַּמַּאֲפִיָּה אוֹפִים {a} מַגָּשִׁים. עַל כָּל מַגָּשׁ {b} מַאֲפִים. כַּמָּה מַאֲפִים אוֹפִים בְּסַךְ הַכֹּל?"),
    (1, "לְכָל מִשְׁתַּתֵּף בַּחֻג נוֹתְנִים {b} דַּפִּים. בַּחֻג {a} מִשְׁתַּתְּפִים. כַּמָּה דַּפִּים צָרִיךְ לְהָכִין?"),
    (1, "בַּחֲנוּת יֵשׁ {a} מַדָּפִים שֶׁל צַעֲצוּעִים. עַל כָּל מַדָּף {b} צַעֲצוּעִים. כַּמָּה צַעֲצוּעִים יֵשׁ עַל הַמַּדָּפִים?"),
    (1, "בְּכָל מַסְלוּל בַּמִּשְׂחָק יֵשׁ {b} תַּחֲנוֹת. בָּנוּ {a} מַסְלוּלִים נִפְרָדִים. כַּמָּה תַּחֲנוֹת יֵשׁ בְּסַךְ הַכֹּל?"),
    (1, "בְּכָל קֻפְסַת יְצִירָה יֵשׁ {b} מִכְחוֹלִים. הֵבִיאוּ {a} קֻפְסָאוֹת לַכִּתָּה. כַּמָּה מִכְחוֹלִים הֵבִיאוּ?"),
    (1, "לְכָל שֻׁלְחָן מְכִינִים {b} מַפִּיּוֹת. בָּאוּלָם {a} שֻׁלְחָנוֹת. כַּמָּה מַפִּיּוֹת יֵשׁ לְהָכִין?"),
    (1, "הַגַּנָּן שָׁתַל {a} שׁוּרוֹת שֶׁל שְׁתִילִים. בְּכָל שׁוּרָה {b} שְׁתִילִים. כַּמָּה שְׁתִילִים שָׁתַל?"),
    (1, "בְּכָל תֵּבָה יֵשׁ {b} אוֹצָרוֹת. בַּמִּשְׂחָק מָצְאוּ {a} תֵּבוֹת. כַּמָּה אוֹצָרוֹת מָצְאוּ בְּסַךְ הַכֹּל?"),
    # Level C: infer equal groups from a longer context. No extra operation is needed.
    (2, "לְקִשּׁוּט הַכִּתָּה מְכִינִים שַׁרְשְׁרוֹת זֵהוֹת. כָּל שַׁרְשֶׁרֶת מֻרְכֶּבֶת מִ־{b} טַבָּעוֹת נְיָר. רוֹצִים לִתְלוֹת {a} שַׁרְשְׁרוֹת. כַּמָּה טַבָּעוֹת צָרִיךְ לְהָכִין?"),
    (2, "בְּמִשְׂחַק הָאוֹצָר כָּל הַצְלָחָה מְזַכָּה בְּ־{b} נְקֻדּוֹת. שָׁקֵד הִצְלִיחָה בְּ־{a} מְשִׂימוֹת, וְלֹא קִבְּלָה נְקֻדּוֹת נוֹסָפוֹת. כַּמָּה נְקֻדּוֹת צָבְרָה?"),
    (2, "מוֹכְרִים כַּרְטִיסִים בַּחֲבִילוֹת שֶׁל {b} כַּרְטִיסִים. הַמּוֹרָה קָנְתָה {a} חֲבִילוֹת שְׁלֵמוֹת. לְכַמָּה יְלָדִים יֵשׁ כַּרְטִיס, אִם כָּל יֶלֶד מְקַבֵּל אֶחָד?"),
    (2, "לְהַכָּנַת דֶּגֶם אֶחָד צָרִיךְ {b} חֲלָקִים. הַכִּתָּה בּוֹנָה {a} דְּגָמִים זֵהִים, בְּלִי לְשַׁתֵּף חֲלָקִים בֵּינֵיהֶם. כַּמָּה חֲלָקִים צָרִיךְ בְּסַךְ הַכֹּל?"),
    (2, "בְּלֻחַ הַתְּמוּנוֹת יֵשׁ {a} שׁוּרוֹת, וּבְכָל שׁוּרָה {b} מְקוֹמוֹת. מַדְבִּיקִים תְּמוּנָה אַחַת בְּכָל מָקוֹם וּמְמַלְּאִים אֶת הַלּוּחַ. כַּמָּה תְּמוּנוֹת צָרִיךְ?"),
    (2, "בְּתַחֲרוּת יֵשׁ {a} קְבוּצוֹת שָׁווֹת בְּגָדְלָן. בְּכָל קְבוּצָה {b} יְלָדִים. כָּל יֶלֶד מְקַבֵּל מְדַלְיָה אַחַת. כַּמָּה מְדַלְיוֹת צָרִיךְ לְכָל הַיְּלָדִים?"),
    (2, "מְסַדְּרִים {a} קֻפְסָאוֹת מַתָּנָה. בְּכָל קֻפְסָה אוֹתוֹ מִסְפַּר מַדְבֵּקוֹת: {b}. כַּמָּה מַדְבֵּקוֹת יֵשׁ לְהוֹצִיא מֵהַמְּגֵרָה כְּדֵי לְמַלֵּא אֶת כָּל הַקֻּפְסָאוֹת?"),
    (2, "בְּכָל יוֹם שָׁקֵד פּוֹתֶרֶת {b} תַּרְגִּילִים. הִיא הִתְמִידָה בְּכָךְ בְּמֶשֶׁךְ {a} יָמִים בְּדִיּוּק. כַּמָּה תַּרְגִּילִים פָּתְרָה בִּתְקוּפָה זוֹ?"),
    (2, "לְכָל תַּחֲנַת יְצִירָה מַקְצִיבִים {b} צְבָעִים. בַּחֲצַר פּוֹעֲלוֹת {a} תַּחֲנוֹת, וְהַצְּבָעִים נִשְׁאָרִים בְּכָל תַּחֲנָה. כַּמָּה צְבָעִים צָרִיךְ לְהָבִיא לַחֲצַר?"),
    (2, "בְּסֵפֶר יֵשׁ {a} פְּרָקִים בְּאוֹתוֹ אֹרֶךְ. כָּל פֶּרֶק מֵכִיל {b} עַמּוּדִים. כַּמָּה עַמּוּדִים יֵשׁ בְּכָל הַפְּרָקִים יַחַד, בְּלִי לִסְפֹּר אֶת הַכְּרִיכָה?"),
    (2, "רוֹצִים לְמַלֵּא {a} מַגָּשִׁים. בְּכָל מַגָּשׁ יֵשׁ מָקוֹם לְ־{b} מַאֲפִים. כָּל הַמַּגָּשִׁים צְרִיכִים לִהְיוֹת מְלֵאִים. כַּמָּה מַאֲפִים צָרִיךְ לֶאֱפוֹת?"),
    (2, "בְּכָל סַבָּב שֶׁל הַמִּשְׂחָק אוֹסְפִים {b} אֲבָנִים. מְשַׂחֲקִים {a} סְבָבִים וְשׁוֹמְרִים אֶת כָּל הָאֲבָנִים שֶׁנֶּאֶסְפוּ. כַּמָּה אֲבָנִים יִהְיוּ בַּסּוֹף?"),
]

def build_word_bank():
    pairs = {
        0: [(a,b) for a in (2,3,4,5) for b in range(2,6)],
        1: [(a,b) for a in range(2,11) for b in range(2,11)],
        2: [(a,b) for a in range(6,11) for b in range(3,11)],
    }
    bank=[]
    for t,(level,template) in enumerate(STORY_TEMPLATES):
        choices=pairs[level]
        for variant in range(5):
            a,b=choices[(t*7+variant*3)%len(choices)]
            bank.append(dict(id=f'w{len(bank)+1:03}',level=level,text=template.format(a=a,b=b),a=a,b=b))
    assert len(bank)==200
    assert len({q['text'] for q in bank})==200
    return bank

WORD_BANK=build_word_bank()
WORDS_BY_ID={q['id']:q for q in WORD_BANK}


"""Server-owned accounts, attempts, grading and shared class leaderboards."""
import hashlib
import hmac
import json
import math
import os
import random
import re
import secrets
import sqlite3
import time
import unicodedata
import uuid
from contextlib import contextmanager
from pathlib import Path



GAME_TOTALS = {'quick': (20,20,20), 'words': (20,20,20), 'maze': (10,15,20)}
ACTIVITIES = ('quick','words','maze','table')
RNG = random.SystemRandom()
PIN_ITERATIONS = 310_000

class UserError(Exception):
    """A safe, user-facing validation error. Never includes credentials."""

def canonical(text):
    text=unicodedata.normalize('NFKC', str(text))
    text=''.join(c for c in text if not unicodedata.combining(c))
    return ' '.join(text.split()).casefold()

def clean_name(value,label,maxlen=32):
    if not isinstance(value,str): raise UserError('יֵשׁ לְמַלֵּא אֶת כָּל הַפְּרָטִים.')
    value=' '.join(unicodedata.normalize('NFKC',value).split())
    if not 1<=len(value)<=maxlen or not any(c.isalnum() for c in value) or any(unicodedata.category(c)[0] not in 'LMN' and c not in " -'׳״." for c in value):
        raise UserError(f'{label}: נַקְלִיד טֶקְסְט קָצָר וְתַקִּין.')
    return value

def canonical_class(text):
    return re.sub(r"[\s'\"׳״.\-]",'',canonical(text))

def identity(first,last,school_class):
    return hashlib.sha256('\x1f'.join((canonical(first),canonical(last),canonical_class(school_class))).encode()).hexdigest()

def pin_hash(pin,salt):
    return hashlib.pbkdf2_hmac('sha256',pin.encode(),bytes.fromhex(salt),PIN_ITERATIONS).hex()

def encode(value): return json.dumps(value,ensure_ascii=False,separators=(',',':'))

def parse_number(value):
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]{1,3}',value.strip()):
        raise UserError('נַקְלִיד מִסְפָּר שָׁלֵם. הַנִּסָּיוֹן לֹא נִסְפַּר.')
    return int(value.strip())

class Database:
    def __init__(self,url=None,dev_path=None):
        if not url and not dev_path:
            raise ValueError('A dedicated database connection must be configured.')
        self.url=url
        self.dev_path=str(dev_path) if dev_path else None
        self.pg=bool(url)

    @contextmanager
    def transaction(self):
        if self.pg:
            import psycopg
            from psycopg.rows import dict_row
            con=psycopg.connect(self.url,connect_timeout=10,sslmode='require',row_factory=dict_row)
            con.execute('SET search_path TO shaked_private')
        else:
            Path(self.dev_path).parent.mkdir(parents=True,exist_ok=True)
            con=sqlite3.connect(self.dev_path,timeout=20)
            con.row_factory=sqlite3.Row
            con.execute('PRAGMA foreign_keys=ON')
            con.execute('BEGIN IMMEDIATE')
        try:
            yield Connection(con,self.pg)
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def initialize(self):
        # A private PostgreSQL schema is never exposed through Supabase's public Data API.
        if self.pg:
            import psycopg
            with psycopg.connect(self.url,connect_timeout=10,sslmode='require') as con:
                con.execute('CREATE SCHEMA IF NOT EXISTS shaked_private')
                con.execute('REVOKE ALL ON SCHEMA shaked_private FROM PUBLIC')
        with self.transaction() as c:
            for sql in [
                '''CREATE TABLE IF NOT EXISTS players (
                    id TEXT PRIMARY KEY, identity_key TEXT NOT NULL UNIQUE,
                    first_name TEXT NOT NULL,last_name TEXT NOT NULL,class_name TEXT NOT NULL,
                    class_key TEXT NOT NULL,pin_salt TEXT NOT NULL,pin_hash TEXT NOT NULL,
                    created DOUBLE PRECISION NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS login_limits (
                    identity_key TEXT PRIMARY KEY, failures INTEGER NOT NULL,
                    window_start DOUBLE PRECISION NOT NULL,blocked_until DOUBLE PRECISION NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,player_id TEXT NOT NULL REFERENCES players(id),
                    activity TEXT NOT NULL,level INTEGER NOT NULL,status TEXT NOT NULL,
                    data TEXT NOT NULL,created DOUBLE PRECISION NOT NULL,updated DOUBLE PRECISION NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS results (
                    run_id TEXT PRIMARY KEY REFERENCES runs(id),player_id TEXT NOT NULL REFERENCES players(id),
                    activity TEXT NOT NULL,level INTEGER NOT NULL,score DOUBLE PRECISION NOT NULL,
                    first_correct INTEGER NOT NULL,total INTEGER NOT NULL,passed INTEGER NOT NULL,
                    finished DOUBLE PRECISION NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS processed_requests (
                    player_id TEXT NOT NULL REFERENCES players(id),request_id TEXT NOT NULL,
                    created DOUBLE PRECISION NOT NULL,PRIMARY KEY(player_id,request_id))''',
                'CREATE INDEX IF NOT EXISTS runs_player_activity ON runs(player_id,activity,created)',
                'CREATE INDEX IF NOT EXISTS results_player ON results(player_id)',
                'CREATE INDEX IF NOT EXISTS players_class ON players(class_key)',
            ]: c.execute(sql)

class Connection:
    def __init__(self,con,pg): self.con,self.pg=con,pg
    def execute(self,sql,args=()):
        return self.con.execute(sql.replace('?','%s') if self.pg else sql,args)
    def one(self,sql,args=()):
        row=self.execute(sql,args).fetchone()
        return dict(row) if row is not None else None
    def all(self,sql,args=()): return [dict(row) for row in self.execute(sql,args).fetchall()]
    def lock_player(self,pid):
        return self.one('SELECT * FROM players WHERE id=?'+(' FOR UPDATE' if self.pg else ''),(pid,))

def make_maze():
    grid=[[1]*9 for _ in range(9)]
    grid[1][1]=0
    stack=[(1,1)]
    while stack:
        x,y=stack[-1]
        options=[(dx,dy) for dx,dy in ((2,0),(-2,0),(0,2),(0,-2))
                 if 0<x+dx<8 and 0<y+dy<8 and grid[y+dy][x+dx]]
        if not options: stack.pop();continue
        dx,dy=RNG.choice(options)
        grid[y+dy//2][x+dx//2]=0
        grid[y+dy][x+dx]=0
        stack.append((x+dx,y+dy))
    queue=[(1,1)];dist={(1,1):0}
    for x,y in queue:
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<9 and 0<=ny<9 and not grid[ny][nx] and (nx,ny) not in dist:
                dist[nx,ny]=dist[x,y]+1;queue.append((nx,ny))
    gx,gy=max(dist,key=dist.get)
    return dict(grid=grid,goal={'x':gx,'y':gy},x=1,y=1,moves=0,pending=False,lives=3,
                visited=[i==10 for i in range(81)])

def question_pool(activity,level):
    if activity=='words': return [q['id'] for q in WORD_BANK if q['level']==level]
    factors=(range(1,6),range(2,11),range(6,11))[level]
    return [f'q{a}-{b}' for a in factors for b in range(1,11)]

def question_data(qid):
    if qid.startswith('w'): return WORDS_BY_ID[qid]
    a,b=map(int,qid[1:].split('-'))
    return {'id':qid,'a':a,'b':b,'text':None}

class Classroom:
    def __init__(self,db): self.db=db

    def authenticate(self,mode,payload):
        first=clean_name(payload.get('first'),'שֵׁם פְּרָטִי')
        last=clean_name(payload.get('last'),'שֵׁם מִשְׁפָּחָה')
        group=clean_name(payload.get('class_name'),'כִּתָּה',24)
        pin=payload.get('pin')
        if not isinstance(pin,str) or not re.fullmatch('[0-9]{4}',pin):
            raise UserError('הַקּוֹד צָרִיךְ לְהָכִיל אַרְבַּע סְפָרוֹת בְּדִיּוּק.')
        key=identity(first,last,group);now=time.time();error=None;pid=None
        with self.db.transaction() as c:
            c.execute('INSERT INTO login_limits(identity_key,failures,window_start,blocked_until) VALUES(?,0,?,0) ON CONFLICT(identity_key) DO NOTHING',(key,now))
            limit=c.one('SELECT * FROM login_limits WHERE identity_key=?'+(' FOR UPDATE' if c.pg else ''),(key,))
            if limit['blocked_until']>now:
                error='הָיוּ כַּמָּה נִסְיוֹנוֹת כְּנִיסָה שְׁגוּיִים. נְנַסֶּה שׁוּב בְּעוֹד כַּמָּה דַּקּוֹת.'
            else:
                player=c.one('SELECT * FROM players WHERE identity_key=?',(key,))
                if mode=='register':
                    if player: error='הַשֵּׁם וְהַכִּתָּה כְּבָר רְשׁוּמִים. נִבְחַר בִּכְנִיסָה לְשַׂחְקָן קַיָּם.'
                    else:
                        pid=str(uuid.uuid4());salt=secrets.token_hex(16)
                        c.execute('INSERT INTO players(id,identity_key,first_name,last_name,class_name,class_key,pin_salt,pin_hash,created) VALUES(?,?,?,?,?,?,?,?,?)',
                                  (pid,key,first,last,group,canonical_class(group),salt,pin_hash(pin,salt),now))
                elif mode=='login':
                    digest=pin_hash(pin,player['pin_salt'] if player else '0'*32)
                    if player and hmac.compare_digest(digest,player['pin_hash']):
                        pid=player['id']
                        c.execute('UPDATE login_limits SET failures=0,window_start=?,blocked_until=0 WHERE identity_key=?',(now,key))
                    else:
                        failures=limit['failures']+1 if now-limit['window_start']<900 else 1
                        started=limit['window_start'] if now-limit['window_start']<900 else now
                        c.execute('UPDATE login_limits SET failures=?,window_start=?,blocked_until=? WHERE identity_key=?',
                                  (failures,started,now+900 if failures>=5 else 0,key))
                        error='הַפְּרָטִים אוֹ הַקּוֹד אֵינָם תּוֹאֲמִים. נִבְדֹּק וּנְנַסֶּה שׁוּב.'
                else: error='פְּעֻלַּת כְּנִיסָה לֹא תַּקִּינָה.'
        if error: raise UserError(error)
        return pid

    def unlocked(self,c,pid):
        opened={a:0 for a in GAME_TOTALS}
        for r in c.all('SELECT activity,MAX(level) AS level FROM results WHERE player_id=? AND passed=1 GROUP BY activity',(pid,)):
            if r['activity'] in opened: opened[r['activity']]=min(2,int(r['level'])+1)
        return opened

    def latest(self,c,pid,activity):
        row=c.one('SELECT * FROM runs WHERE player_id=? AND activity=? ORDER BY created DESC,id DESC LIMIT 1',(pid,activity))
        if row: row['data']=json.loads(row['data'])
        return row

    def _save_run(self,c,run):
        c.execute('UPDATE runs SET data=?,status=?,updated=? WHERE id=?',(encode(run['data']),run['status'],time.time(),run['id']))

    def _new_run(self,c,pid,activity,level):
        if activity=='table': data={'values':['']*100,'marks':['']*100,'first':[None]*100,'first_correct':0,'completed':0}
        else:
            total=GAME_TOTALS[activity][level]
            data={'questions':RNG.sample(question_pool(activity,level),total),'index':0,'tries':0,'solved':False,
                  'revealed':False,'first_correct':0,'completed':0,'points':0,'last_answer':''}
            if activity=='maze': data.update(make_maze())
        now=time.time()
        run={'id':str(uuid.uuid4()),'player_id':pid,'activity':activity,'level':level,'status':'active','data':data,'created':now}
        c.execute('INSERT INTO runs(id,player_id,activity,level,status,data,created,updated) VALUES(?,?,?,?,?,?,?,?)',
                  (run['id'],pid,activity,level,'active',encode(data),now,now))
        return run

    def _finish(self,c,run,ending='complete'):
        data=run['data'];activity=run['activity']
        total=100 if activity=='table' else GAME_TOTALS[activity][run['level']]
        score=round(data['first_correct']/total*100,2)
        passed=ending=='complete' and score>=80
        run['status']='lost' if ending=='lost' else ('passed' if passed else 'retry')
        data['score']=score
        c.execute('INSERT INTO results(run_id,player_id,activity,level,score,first_correct,total,passed,finished) VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(run_id) DO NOTHING',
                  (run['id'],run['player_id'],activity,run['level'],score,data['first_correct'],total,int(passed),time.time()))
        self._save_run(c,run)

    def _owned_run(self,c,pid,payload):
        rid=payload.get('run_id')
        if not isinstance(rid,str): raise UserError('נִרְעֲנֵן אֶת הַמִּשְׂחָק וְנַמְשִׁיךְ.')
        row=c.one('SELECT * FROM runs WHERE id=? AND player_id=?',(rid,pid))
        if not row: raise UserError('הַמִּשְׂחָק אֵינוֹ זָמִין לַשַּׂחְקָן הַזֶּה.')
        row['data']=json.loads(row['data'])
        return row

    def _current_question(self,run,payload):
        d=run['data']
        if run['activity']=='table' or d['index']>=len(d['questions']): raise UserError('הַסֶּבֶב כְּבָר הֻשְׁלַם.')
        key=f"{run['id']}:{d['index']}"
        if payload.get('question_key')!=key: raise UserError('הַשְּׁאֵלָה הִתְעַדְּכְנָה. נַעֲנֶה עַל הַשְּׁאֵלָה הַמֻּצֶּגֶת.')
        return question_data(d['questions'][d['index']])

    def _answer(self,c,run,payload):
        d=run['data'];activity=run['activity']
        if run['status']!='active': return False
        if activity=='maze' and not d['pending']: raise UserError('קֹדֶם מִתְקַדְּמִים בַּמָּבוֹךְ.')
        q=self._current_question(run,payload)
        if d['solved']: return False
        if activity=='maze' and d['revealed']: return False
        answer=parse_number(payload.get('answer'))
        d['last_answer']=str(answer)
        good=answer==q['a']*q['b']
        if good:
            if d['tries']==0: d['first_correct']+=1
            d['points']+=10 if d['tries']==0 else 5
            d['solved']=True;d['completed']+=1
            if activity=='maze':
                self._advance_maze_question(c,run)
            elif d['completed']==20: self._finish(c,run)
        else:
            d['tries']+=1
            if activity=='maze':
                d['lives']=max(0,3-d['tries'])
            if d['tries']>=3: d['revealed']=True
        self._save_run(c,run)
        return good

    def _next(self,c,run,payload):
        if run['status']!='active': return
        if run['activity'] not in ('quick','words'): raise UserError('פְּעֻלָּה לֹא מַתְאִימָה לַמִּשְׂחָק.')
        self._current_question(run,payload)
        d=run['data']
        if not d['solved']: raise UserError('קֹדֶם נַקְלִיד תְּשׁוּבָה נְכוֹנָה לַשְּׁאֵלָה הַזֹּאת.')
        d.update(index=d['index']+1,tries=0,solved=False,revealed=False,last_answer='')
        self._save_run(c,run)

    def _advance_maze_question(self,c,run):
        d=run['data']
        d.update(index=d['index']+1,tries=0,solved=False,revealed=False,last_answer='',
                 pending=False,moves=0,lives=3)
        self._maze_finish_if_ready(c,run)

    def _maze_continue(self,c,run,payload):
        if run['activity']!='maze': raise UserError('פְּעֻלָּה לֹא מַתְאִימָה לַמִּשְׂחָק.')
        if run['status']!='active': return
        self._current_question(run,payload)
        d=run['data']
        if not d['pending'] or not d['revealed'] or d['tries']<3:
            raise UserError('קֹדֶם נַעֲנֶה עַל הַשְּׁאֵלָה הַמֻּצֶּגֶת.')
        # Acknowledging the shown solution completes this question without points.
        d['completed']+=1
        self._advance_maze_question(c,run)
        self._save_run(c,run)

    def _maze_finish_if_ready(self,c,run):
        d=run['data']
        if d['completed']==len(d['questions']) and not d['pending'] and (d['x'],d['y'])==(d['goal']['x'],d['goal']['y']):
            self._finish(c,run)

    def _move(self,c,run,payload):
        d=run['data']
        if run['activity']!='maze' or run['status']!='active' or d['pending']: return
        delta={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}.get(payload.get('direction'))
        if delta is None: raise UserError('כִּוּוּן לֹא תַּקִּין.')
        nx,ny=d['x']+delta[0],d['y']+delta[1]
        if not (0<=nx<9 and 0<=ny<9) or d['grid'][ny][nx]: return
        d['x']=nx;d['y']=ny;d['visited'][ny*9+nx]=True
        if d['completed']<len(d['questions']):
            d['moves']+=1
            if d['moves']==3: d['pending']=True
        self._maze_finish_if_ready(c,run)
        self._save_run(c,run)

    def _table(self,c,pid,action,payload):
        run=self.latest(c,pid,'table') or self._new_run(c,pid,'table',0)
        if payload.get('run_id') and payload['run_id']!=run['id']:
            raise UserError('הַלּוּחַ הִתְעַדְּכֵן בְּמָקוֹם אַחֵר. נִטְעַן אֶת הַגִּרְסָה הָאַחֲרוֹנָה.')
        if action=='table_clear':
            # A reset abandons an unfinished table; only completed boards are ranked.
            if run['status']=='active':
                run['status']='abandoned'
                self._save_run(c,run)
            if run['status']!='active': run=self._new_run(c,pid,'table',0)
            else: run['data'].update(values=['']*100,marks=['']*100,first=[None]*100)
            self._save_run(c,run);return False
        if run['status']!='active': return False
        values=payload.get('values')
        if not isinstance(values,list) or len(values)!=100 or any(not isinstance(v,str) or len(v)>3 for v in values):
            raise UserError('נִרְעֲנֵן אֶת הַלּוּחַ וְנַמְשִׁיךְ.')
        d=run['data'];filled=correct=0
        for i,value in enumerate(values):
            value=value.strip();expected=(i//10+1)*(i%10+1)
            good=bool(re.fullmatch('[0-9]{1,3}',value)) and int(value)==expected
            if value!=d['values'][i]: d['marks'][i]=''
            d['values'][i]=value
            if action=='table_clear_wrong':
                if value and not good: d['values'][i]='';d['marks'][i]=''
            elif action=='table_check':
                if value:
                    filled+=1;correct+=int(good)
                    if d['first'][i] is None: d['first'][i]=bool(good)
                    d['marks'][i]='correct' if good else 'wrong'
                else: d['marks'][i]=''
        d['first_correct']=sum(x is True for x in d['first'])
        d['completed']=sum(v=='correct' for v in d['marks'])
        if action=='table_check' and filled==correct==100: self._finish(c,run)
        self._save_run(c,run)
        return action=='table_check' and filled>0 and filled==correct

    def perform(self,pid,action,payload,request_id):
        if not isinstance(payload,dict): raise UserError('פְּעֻלָּה לֹא תַּקִּינָה.')
        if not isinstance(request_id,str) or not re.fullmatch('[A-Za-z0-9_-]{8,100}',request_id):
            raise UserError('נִרְעֲנֵן אֶת הַדַּף וְנַמְשִׁיךְ.')
        celebrate=False
        with self.db.transaction() as c:
            if not c.lock_player(pid): raise UserError('נִכָּנֵס שׁוּב לַמִּשְׂחָק.')
            done=c.one('SELECT request_id FROM processed_requests WHERE player_id=? AND request_id=?',(pid,request_id))
            if not done and action!='sync':
                if action=='start':
                    activity=payload.get('activity');level=payload.get('level')
                    if activity not in GAME_TOTALS or type(level) is not int or level not in (0,1,2):
                        raise UserError('רָמָה לֹא תַּקִּינָה.')
                    if level>self.unlocked(c,pid)[activity]:
                        raise UserError('קֹדֶם נְסַיֵּם אֶת הָרָמָה הַקּוֹדֶמֶת עִם לְפָחוֹת 80% הַצְלָחָה.')
                    latest=self.latest(c,pid,activity)
                    if not latest or latest['status']!='active': self._new_run(c,pid,activity,level)
                elif action.startswith('table_') and action in ('table_save','table_check','table_clear_wrong','table_clear'):
                    celebrate=self._table(c,pid,action,payload)
                elif action in ('answer','next','move','maze_continue','maze_restart'):
                    run=self._owned_run(c,pid,payload)
                    if action=='answer': celebrate=self._answer(c,run,payload)
                    elif action=='next': self._next(c,run,payload)
                    elif action=='move': self._move(c,run,payload)
                    elif action=='maze_continue': self._maze_continue(c,run,payload)
                    elif action=='maze_restart':
                        if run['activity']!='maze': raise UserError('פְּעֻלָּה לֹא תַּקִּינָה.')
                        latest=self.latest(c,pid,'maze')
                        if latest['id']!=run['id']: raise UserError('הַמִּשְׂחָק הִתְעַדְּכֵן. נַמְשִׁיךְ מֵהַמַּצָּב הַנּוֹכְחִי.')
                        if run['status']=='active':
                            run['status']='abandoned';self._save_run(c,run)
                        self._new_run(c,pid,'maze',run['level'])
                else: raise UserError('פְּעֻלָּה לֹא תַּקִּינָה.')
                c.execute('INSERT INTO processed_requests(player_id,request_id,created) VALUES(?,?,?)',(pid,request_id,time.time()))
                c.execute('DELETE FROM processed_requests WHERE player_id=? AND created<?',(pid,time.time()-86400*7))
            return {'snapshot':self._snapshot(c,pid),'celebrate':bool(celebrate and not done)}

    def snapshot(self,pid):
        with self.db.transaction() as c: return self._snapshot(c,pid)

    def _public_run(self,run):
        d=run['data'];activity=run['activity']
        result={k:run[k] for k in ('id','activity','level','status')}
        result.update(first_correct=d['first_correct'],completed=d['completed'],score=d.get('score'),
                      total=100 if activity=='table' else len(d['questions']))
        if activity=='table':
            result.update(values=d['values'],marks=d['marks'])
            return result
        result.update(index=d['index'],tries=d['tries'],solved=d['solved'],points=d['points'],revealed=d['revealed'])
        if d['index']<len(d['questions']):
            q=question_data(d['questions'][d['index']])
            result['question']={'key':f"{run['id']}:{d['index']}",'text':q['text']}
            if activity!='words': result['question'].update(a=q['a'],b=q['b'])
            if d['revealed']: result['question']['answer']=q['a']*q['b']
        if activity=='maze':
            result.update({k:d[k] for k in ('grid','goal','x','y','moves','pending','lives','visited')})
            if run['status']=='active': result['lives']=max(0,3-d['tries'])
        return result

    def _snapshot(self,c,pid):
        player=c.one('SELECT id,first_name,last_name,class_name,class_key FROM players WHERE id=?',(pid,))
        if not player: raise UserError('נִכָּנֵס שׁוּב לַמִּשְׂחָק.')
        board=c.all('''SELECT p.id,p.first_name,p.last_name,p.class_name,COUNT(r.run_id) AS games,AVG(r.score) AS average
            FROM players p JOIN results r ON r.player_id=p.id WHERE p.class_key=?
            GROUP BY p.id,p.first_name,p.last_name,p.class_name
            ORDER BY AVG(r.score) DESC,p.first_name,p.last_name,p.id LIMIT 500''',(player['class_key'],))
        previous=None;rank=0
        for row in board:
            row['average']=round(float(row['average']),2)
            if previous!=row['average']: rank+=1;previous=row['average']
            row['rank']=rank;row['self']=row['id']==pid;del row['id']
        stats=c.one('SELECT COUNT(run_id) AS games,AVG(score) AS average FROM results WHERE player_id=?',(pid,))
        stats['average']=round(float(stats['average']),2) if stats['average'] is not None else None
        recent=c.all('SELECT activity,level,score,first_correct,total,passed,finished FROM results WHERE player_id=? ORDER BY finished DESC LIMIT 30',(pid,))
        runs={a:self.latest(c,pid,a) for a in ACTIVITIES}
        return {'player':{k:player[k] for k in ('id','first_name','last_name','class_name')},
                'stats':stats,'leaderboard':board,'recent':recent,'unlocked':self.unlocked(c,pid),
                'runs':{a:self._public_run(r) if r else None for a,r in runs.items()},
                'bank_counts':[sum(q['level']==i for q in WORD_BANK) for i in range(3)]}


APP_HTML = r'''<!doctype html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <meta name="theme-color" content="#f7f5ee" />
    <title>לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא</title>
    <style>
      :root {
        color-scheme: light;
        --ink: #243c3a;
        --muted: #627571;
        --paper: #f7f5ee;
        --white: #fffefa;
        --green: #187568;
        --line: #dce4dd;
        --violet: #7860aa;
        --good: #d0f0df;
        --bad: #ffdadd;
        --shadow: 0 8px 28px #243c3a09;
      }
      * {
        box-sizing: border-box;
      }
      html,
      body {
        margin: 0;
        padding: 0;
        background: var(--paper);
        color: var(--ink);
        font-family: Arial, "Noto Sans Hebrew", sans-serif;
        direction: rtl;
        text-align: right;
      }
      body {
        overflow-x: hidden;
      }
      button,
      input {
        font: inherit;
      }
      button {
        cursor: pointer;
        touch-action: manipulation;
      }
      button:disabled {
        cursor: default;
        opacity: 0.48;
      }
      button,
      input,
      a {
        -webkit-tap-highlight-color: transparent;
      }
      button:focus-visible,
      input:focus-visible,
      a:focus-visible {
        outline: 3px solid #e59f32;
        outline-offset: 3px;
      }
      button {
        border: 0;
      }
      h1,
      h2,
      h3,
      p {
        margin-top: 0;
      }
      h1,
      h2,
      h3 {
        line-height: 1.5;
        letter-spacing: -0.025em;
      }
      p {
        line-height: 1.8;
      }
      h2 {
        font-size: clamp(22px, 4vw, 30px);
        margin-bottom: 6px;
      }
      h3 {
        font-size: 20px;
      }
      bdi,
      .num,
      .math,
      input.numeric {
        direction: ltr;
        unicode-bidi: isolate;
        text-align: left;
        font-variant-numeric: tabular-nums;
      }
      bdi {
        display: inline-block;
      }
      .math {
        display: block;
        font-size: clamp(30px, 6vw, 48px);
        font-weight: 700;
        letter-spacing: 0.025em;
        line-height: 1.5;
      }
      .num {
        display: inline-block;
      }
      input.numeric {
        text-align: left !important;
      }
      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }
      input {
        font-size: 18px;
      }
      input.numeric {
        border: 2px solid var(--line);
        border-radius: 12px;
        background: white;
        padding: 12px;
        width: 100%;
        min-height: 50px;
        color: var(--ink);
      }
      input.numeric:focus {
        border-color: var(--green);
      }
      [hidden] {
        display: none !important;
      }
      .app {
        max-width: 1040px;
        margin: 0 auto;
        padding: 20px 24px 32px;
      }
      .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
      }
      .brand-mark {
        width: 44px;
        height: 44px;
        border-radius: 15px;
        background: var(--green);
        color: white;
        display: grid;
        place-items: center;
        font-size: 30px;
        flex-shrink: 0;
      }
      .brand-name {
        font-size: 18px;
        font-weight: 700;
        line-height: 1.6;
      }
      .brand-note {
        font-size: 13px;
        color: var(--muted);
      }
      .tag {
        color: var(--green);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.04em;
      }
      .nav {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        padding: 8px 0 16px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 24px;
      }
      .nav button {
        background: transparent;
        color: var(--muted);
        padding: 10px 14px;
        border-radius: 24px;
        font-size: 15px;
        font-weight: 700;
        min-height: 42px;
        white-space: nowrap;
      }
      .nav button.active {
        background: var(--ink);
        color: #fff;
      }
      .nav button:hover:not(.active) {
        background: #e9eee7;
      }
      .hero {
        display: grid;
        grid-template-columns: 1.55fr 1fr;
        gap: 20px;
        align-items: center;
        padding: 22px 0 32px;
      }
      .hero h1 {
        font-size: clamp(30px, 5vw, 47px);
        margin: 12px 0 16px;
        max-width: 650px;
      }
      .hero p {
        max-width: 590px;
        font-size: 18px;
        color: var(--muted);
        margin-bottom: 0;
      }
      .hero-art {
        position: relative;
        height: 230px;
        display: grid;
        place-items: center;
      }
      .orb {
        width: 195px;
        height: 195px;
        border-radius: 50%;
        background: #e8eddc;
        display: grid;
        place-items: center;
        font-size: 70px;
      }
      .float {
        position: absolute;
        border: 1px solid #fff;
        border-radius: 16px;
        background: #fffefa;
        box-shadow: var(--shadow);
        padding: 14px 19px;
        font-size: 23px;
        font-weight: bold;
        transform: rotate(-8deg);
        direction: ltr;
        text-align: left;
      }
      .float.one {
        right: 6px;
        top: 35px;
        color: var(--green);
      }
      .float.two {
        left: 0;
        bottom: 30px;
        color: var(--violet);
        transform: rotate(7deg);
      }
      .section-kicker {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin: 2px 0 14px;
      }
      .section-kicker h2 {
        font-size: 21px;
      }
      .section-kicker span {
        color: var(--muted);
        font-size: 13px;
      }
      .activities {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
      }
      .activity {
        background: var(--white);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 23px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        box-shadow: var(--shadow);
      }
      .activity-top {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
      }
      .activity-icon {
        width: 43px;
        height: 43px;
        border-radius: 14px;
        display: grid;
        place-items: center;
        font-size: 24px;
        background: #e9f1e6;
      }
      .activity:nth-child(2) .activity-icon {
        background: #fff1d0;
      }
      .activity:nth-child(3) .activity-icon {
        background: #eee8f8;
      }
      .activity:nth-child(4) .activity-icon {
        background: #e3f0ed;
      }
      .activity h3 {
        margin: 0;
      }
      .activity p {
        font-size: 16px;
        color: var(--muted);
        flex: 1;
        margin-bottom: 20px;
      }
      .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: var(--green);
        color: white;
        border: 1px solid transparent;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 16px;
        font-weight: 700;
        min-height: 48px;
        line-height: 1.5;
        text-align: right;
      }
      .btn.secondary {
        background: #edf1e9;
        color: var(--ink);
        border-color: #d9e2d8;
      }
      .btn.soft {
        background: white;
        color: var(--muted);
        border-color: var(--line);
      }
      .btn.danger {
        color: #983f4a;
        background: #fff4f2;
        border-color: #f0d8d9;
      }
      .activity .btn {
        width: 100%;
        justify-content: space-between;
      }
      .page-heading {
        margin-bottom: 20px;
      }
      .page-heading p {
        color: var(--muted);
        margin-bottom: 0;
      }
      .panel {
        border: 1px solid var(--line);
        border-radius: 20px;
        background: var(--white);
        padding: 22px;
        box-shadow: var(--shadow);
      }
      .toolbar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 14px;
      }
      .subtle {
        font-size: 14px;
        color: var(--muted);
        line-height: 1.7;
      }
      .status {
        border-radius: 12px;
        padding: 12px 15px;
        line-height: 1.8;
        margin-top: 14px;
        background: #edf1e9;
      }
      .status.success {
        background: var(--good);
        color: #14553b;
      }
      .status.error {
        background: var(--bad);
        color: #8a2738;
      }
      .status.warning {
        background: #fff0cc;
        color: #7a5109;
      }
      .status:empty {
        display: none;
      }
      .actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 16px;
      }
      .actions .btn {
        flex: 1;
      }
      .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        font-size: 13px;
        color: var(--muted);
        margin: 12px 0 0;
      }
      .legend span {
        display: inline-flex;
        align-items: center;
        gap: 5px;
      }
      .dot {
        width: 11px;
        height: 11px;
        border-radius: 4px;
        background: var(--good);
        border: 1px solid #60a881;
      }
      .dot.red {
        background: var(--bad);
        border-color: #d97d8c;
      }
      .dot.neutral {
        background: white;
        border-color: var(--line);
      }
      /* Eleven equal columns and square cells preserve the spreadsheet proportions.
   The optional large-cell view scrolls inside its own container, never the page. */
      .table-scroll {
        width: 100%;
        overflow-x: auto;
        border: 1px solid #bdcfc5;
        border-radius: 12px;
        direction: ltr;
        overscroll-behavior-x: contain;
        -webkit-overflow-scrolling: touch;
      }
      .times-table {
        display: grid;
        grid-template-columns: repeat(11, minmax(0, 1fr));
        width: 100%;
        direction: ltr;
        background: #cddcd2;
        gap: 1px;
      }
      .times-table.large {
        min-width: 610px;
      }
      .table-cell {
        aspect-ratio: 1;
        min-width: 0;
        position: relative;
        background: #fffefa;
        display: flex;
        align-items: stretch;
      }
      .table-cell.head {
        background: #e4eee6;
        color: var(--green);
        font-weight: 700;
        align-items: center;
        justify-content: flex-start;
        padding-left: clamp(2px, 1vw, 10px);
        font-size: clamp(14px, 2.6vw, 19px);
        direction: ltr;
        text-align: left;
      }
      .table-cell.corner {
        background: var(--green);
        color: white;
      }
      .table-cell input {
        border: 0;
        border-radius: 0;
        background: transparent;
        width: 100%;
        min-width: 0;
        min-height: 0;
        padding: 0 2px;
        font-size: clamp(16px, 2.7vw, 24px);
        letter-spacing: -0.045em;
        line-height: 1;
        direction: ltr;
        text-align: left;
        color: var(--ink);
        font-variant-numeric: tabular-nums;
        caret-color: var(--green);
      }
      .table-cell input:focus {
        outline: 3px solid var(--green);
        outline-offset: -3px;
        background: #f5fbf7;
      }
      .table-cell.correct {
        background: var(--good);
        box-shadow: inset 0 -3px #298055;
      }
      .table-cell.wrong {
        background: var(--bad);
        box-shadow: inset 0 -3px #ca5366;
      }
      .table-cell.correct input {
        color: #14553b;
      }
      .table-cell.wrong input {
        color: #8a2738;
      }
      .table-cell.correct:after,
      .table-cell.wrong:after {
        position: absolute;
        right: 2px;
        top: 1px;
        font-size: 9px;
        pointer-events: none;
      }
      .table-cell.correct:after {
        content: "✓";
        color: #14553b;
      }
      .table-cell.wrong:after {
        content: "×";
        color: #8a2738;
      }
      .selected-exercise {
        font-size: 18px;
        font-weight: 700;
        color: var(--green);
        min-width: 90px;
      }
      .score-pill {
        display: flex;
        gap: 8px;
        align-items: center;
        background: #fff2d4;
        border-radius: 25px;
        padding: 8px 14px;
        font-size: 14px;
      }
      .exercise-layout {
        display: grid;
        grid-template-columns: 1.3fr 0.7fr;
        gap: 18px;
      }
      .exercise-card .math {
        margin: 24px 0;
      }
      .answer-form {
        max-width: 460px;
      }
      .answer-form label {
        display: block;
        margin-bottom: 8px;
        font-weight: 700;
      }
      .answer-line {
        display: flex;
        gap: 10px;
        direction: ltr;
      }
      .answer-line input {
        min-width: 0;
        flex: 1;
      }
      .answer-line .btn {
        direction: rtl;
        flex-shrink: 0;
      }
      .note-panel {
        background: #eaf0e5;
        border: 0;
      }
      .note-panel h3 {
        margin-bottom: 10px;
      }
      .note-panel p {
        color: var(--muted);
      }
      .word-question {
        font-size: clamp(20px, 3vw, 27px);
        line-height: 2;
        margin: 22px 0;
      }
      .footer {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.8;
        margin-top: 25px;
        padding-top: 16px;
        border-top: 1px solid var(--line);
      }
      .levels {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin: 18px 0;
      }
      .level {
        background: white;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 13px 10px;
        min-height: 82px;
        color: var(--ink);
        text-align: right;
        line-height: 1.7;
      }
      .level strong {
        display: block;
        font-size: 17px;
      }
      .level small {
        font-size: 13px;
      }
      .level.active {
        border: 2px solid var(--green);
        background: #eaf4ec;
        padding: 12px 9px;
      }
      .maze-layout {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 280px;
        gap: 20px;
        align-items: start;
      }
      .maze-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 12px;
      }
      .hearts {
        font-size: 21px;
        letter-spacing: 2px;
        direction: ltr;
        display: block;
      }
      .progress-track {
        height: 7px;
        background: #e2e9df;
        border-radius: 8px;
        overflow: hidden;
        margin: 10px 0 16px;
        direction: ltr;
      }
      .progress-fill {
        height: 100%;
        background: var(--green);
        border-radius: 8px;
        transition: width 0.2s;
      }
      .maze-arena {
        position: relative;
        max-width: 600px;
        margin: auto;
      }
      .maze-board {
        display: grid;
        grid-template-columns: repeat(9, minmax(0, 1fr));
        gap: 2px;
        aspect-ratio: 1;
        direction: ltr;
        background: #c8dbc2;
        border: 7px solid #c8dbc2;
        border-radius: 18px;
        overflow: hidden;
      }
      .maze-cell {
        display: grid;
        place-items: center;
        position: relative;
        aspect-ratio: 1;
        min-width: 0;
        font-size: clamp(15px, 4vw, 30px);
        background: #efe4ba;
        border-radius: 4px;
      }
      .maze-cell.wall {
        background: #589773;
        box-shadow: inset 0 -3px #407c5c;
      }
      .maze-cell.wall:after {
        content: "♠";
        color: #c3d9b0;
        font-size: clamp(15px, 4vw, 28px);
      }
      .maze-cell.visited:not(.wall):not(.player):not(.goal):after {
        content: "·";
        font-size: 24px;
        color: #b4a362;
      }
      .maze-cell.player {
        background: #ffd27b;
        box-shadow: 0 0 0 2px #dfa747;
        z-index: 1;
      }
      .maze-cell.goal {
        background: #f6d987;
      }
      .maze-caption {
        font-size: 13px;
        color: var(--muted);
        margin-top: 10px;
      }
      .controls-panel {
        padding: 18px;
        background: #f0f3eb;
        border-radius: 18px;
      }
      .dpad {
        display: grid;
        grid-template: repeat(3, 56px) / repeat(3, 56px);
        gap: 8px;
        justify-content: center;
        direction: ltr;
        margin: 14px 0;
      }
      .dpad button {
        border-radius: 15px;
        background: white;
        color: var(--green);
        font-size: 29px;
        font-weight: bold;
        box-shadow: 0 3px 0 #cddace;
        min-width: 0;
      }
      .dpad button:active:not(:disabled) {
        transform: translateY(2px);
        box-shadow: 0 1px 0 #cddace;
      }
      .dpad [data-move="up"] {
        grid-area: 1/2;
      }
      .dpad [data-move="left"] {
        grid-area: 2/1;
      }
      .dpad [data-move="right"] {
        grid-area: 2/3;
      }
      .dpad [data-move="down"] {
        grid-area: 3/2;
      }
      .dpad-center {
        grid-area: 2/2;
        display: grid;
        place-items: center;
        color: #94a595;
        font-size: 24px;
      }
      .maze-overlay {
        position: absolute;
        inset: 0;
        z-index: 5;
        background: #183e35b8;
        backdrop-filter: blur(3px);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 12px;
      }
      .question-box {
        width: 100%;
        max-width: 370px;
        border-radius: 18px;
        background: #fffefa;
        padding: 20px;
        box-shadow: 0 14px 50px #0e332b40;
      }
      .question-box h3 {
        margin: 0 0 6px;
        font-size: 20px;
      }
      .question-box .math {
        font-size: 36px;
        margin: 6px 0 10px;
      }
      .question-box input {
        min-height: 44px;
        padding: 8px;
      }
      .question-box .btn {
        min-height: 44px;
        padding: 8px 12px;
      }
      .question-box .status {
        font-size: 14px;
        margin-top: 9px;
        padding: 8px 10px;
        line-height: 1.5;
      }
      .question-box label {
        font-size: 14px;
        display: block;
        margin-bottom: 5px;
      }
      .end-box {
        text-align: right;
      }
      .end-icon {
        font-size: 48px;
        margin-bottom: 3px;
      }
      .end-box h3 {
        margin-bottom: 5px;
      }
      .end-box p {
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 10px;
      }
      .end-box .btn {
        width: 100%;
        margin-top: 6px;
      }
      .dragon-stage {
        position: relative;
        height: 76px;
        overflow: hidden;
        direction: ltr;
      }
      .dragon-stage .dragon {
        position: absolute;
        left: 5%;
        top: 0;
        font-size: 57px;
        animation: dragon-catch 1.5s ease-out both;
      }
      .dragon-stage .kid {
        position: absolute;
        left: 70%;
        top: 17px;
        font-size: 37px;
        animation: kid-away 1.5s ease-out both;
      }
      @keyframes dragon-catch {
        0% {
          left: -30%;
        }
        65% {
          left: 55%;
          transform: scale(1.1);
        }
        100% {
          left: 110%;
          transform: translateY(-20px);
        }
      }
      @keyframes kid-away {
        0%,
        55% {
          opacity: 1;
          transform: none;
        }
        100% {
          opacity: 0;
          transform: translate(150px, -45px) scale(0.5);
        }
      }
      .fireworks {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 80;
        overflow: hidden;
      }
      .spark {
        position: absolute;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--spark);
        animation: spark 1.1s ease-out var(--delay) both;
      }
      @keyframes spark {
        0% {
          opacity: 0;
          transform: translate(0, 0) scale(0.2);
        }
        10% {
          opacity: 1;
        }
        100% {
          opacity: 0;
          transform: translate(var(--dx), var(--dy)) scale(0.35);
        }
      }
      @media (min-width: 800px) {
        .table-panel {
          max-width: 790px;
          margin: auto;
        }
        .table-cell input {
          padding-left: 7px;
        }
        .table-cell.correct:after,
        .table-cell.wrong:after {
          font-size: 12px;
          right: 4px;
          top: 3px;
        }
      }
      @media (max-width: 760px) {
        .app {
          padding: 16px 14px 24px;
        }
        .hero {
          grid-template-columns: 1fr;
          padding: 8px 0 24px;
        }
        .hero-art {
          display: none;
        }
        .hero h1 {
          font-size: 34px;
          max-width: 540px;
        }
        .hero p {
          font-size: 17px;
        }
        .exercise-layout,
        .maze-layout {
          grid-template-columns: 1fr;
        }
        .controls-panel {
          padding: 14px;
        }
        .dpad {
          margin: 8px 0;
        }
        .controls-panel > p {
          margin-bottom: 8px;
        }
        .note-panel {
          display: none;
        }
        .maze-layout {
          gap: 14px;
        }
        .nav {
          margin-bottom: 20px;
        }
        .nav button {
          padding: 9px 11px;
        }
        .panel {
          padding: 16px;
        }
        .activities {
          gap: 12px;
        }
        .activity {
          padding: 18px;
        }
        .activity h3 {
          font-size: 18px;
        }
      }
      @media (max-width: 480px) {
        .app {
          padding: 12px 10px 24px;
        }
        .brand-note {
          font-size: 12px;
        }
        .brand-name {
          font-size: 16px;
        }
        .brand-row {
          gap: 9px;
        }
        .brand-mark {
          width: 38px;
          height: 38px;
          font-size: 25px;
        }
        .nav {
          gap: 3px;
          padding-top: 3px;
          padding-bottom: 12px;
        }
        .nav button {
          font-size: 13px;
          padding: 8px 9px;
          min-height: 39px;
        }
        .hero h1 {
          font-size: 31px;
        }
        .hero p {
          font-size: 16px;
        }
        .activities {
          grid-template-columns: 1fr;
        }
        .activity {
          padding: 19px;
        }
        .activity p {
          margin-bottom: 14px;
        }
        .section-kicker span {
          display: none;
        }
        .table-panel {
          padding: 8px;
          border-radius: 14px;
        }
        .toolbar {
          gap: 7px;
          margin: 4px 0 10px;
        }
        .toolbar .btn {
          font-size: 13px;
          padding: 8px 10px;
          min-height: 40px;
        }
        .toolbar .subtle {
          font-size: 12px;
        }
        .table-cell input {
          font-size: 16px;
          padding-left: 1px;
          letter-spacing: -0.065em;
        }
        .table-cell.head {
          font-size: 14px;
          padding-left: 2px;
        }
        .table-cell.correct:after,
        .table-cell.wrong:after {
          font-size: 7px;
          right: 1px;
          top: 0;
        }
        .legend {
          font-size: 12px;
          gap: 10px;
          margin-right: 3px;
        }
        .actions {
          gap: 7px;
        }
        .actions .btn {
          font-size: 14px;
          padding: 10px 8px;
          min-height: 48px;
        }
        .actions .btn.primary {
          flex-basis: 100%;
        }
        .table-panel .status {
          font-size: 14px;
        }
        .level {
          padding: 10px 7px;
        }
        .level.active {
          padding: 9px 6px;
        }
        .level strong {
          font-size: 16px;
        }
        .level small {
          font-size: 12px;
        }
        .levels {
          gap: 6px;
        }
        .maze-panel {
          padding: 9px;
        }
        .maze-board {
          border-width: 5px;
          gap: 2px;
        }
        .maze-overlay {
          padding: 9px;
        }
        .question-box {
          padding: 13px;
          border-radius: 14px;
        }
        .question-box h3 {
          font-size: 18px;
        }
        .question-box .math {
          font-size: 30px;
          margin: 4px 0 7px;
        }
        .question-box .status {
          font-size: 13px;
          padding: 6px 8px;
        }
        .question-box .btn {
          font-size: 14px;
        }
        .end-icon {
          font-size: 34px;
        }
        .end-box p {
          font-size: 13px;
        }
        .end-box h3 {
          font-size: 18px;
        }
        .dragon-stage {
          height: 60px;
        }
        .dragon-stage .dragon {
          font-size: 44px;
        }
        .dragon-stage .kid {
          font-size: 28px;
        }
        .answer-line {
          gap: 7px;
        }
        .score-pill {
          font-size: 13px;
          padding: 7px 11px;
        }
        .page-heading {
          margin-bottom: 14px;
        }
        .page-heading p {
          font-size: 15px;
        }
        .maze-stats {
          gap: 6px;
          font-size: 14px;
        }
      }
      @media (max-width: 360px) {
        .table-cell input {
          letter-spacing: -0.12em;
          padding: 0;
          font-size: 16px;
        }
      }
      @media (prefers-reduced-motion: reduce) {
        *,
        *:before,
        *:after {
          animation: none !important;
          transition: none !important;
          scroll-behavior: auto !important;
        }
        .spark {
          display: none;
        }
        .dragon-stage .dragon {
          left: 45%;
        }
        .dragon-stage .kid {
          left: 72%;
        }
      }

.account-strip{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;background:#eaf0e5;border-radius:14px;padding:10px 14px;margin-bottom:14px;font-size:14px;line-height:1.8}
.account-strip .btn{font-size:13px;padding:7px 12px;min-height:38px}.auth-panel{max-width:570px;margin:0 auto}.auth-tabs{display:flex;gap:10px;margin-bottom:20px}.auth-tabs .btn{flex:1}.auth-fields{display:grid;grid-template-columns:1fr 1fr;gap:15px}.auth-fields label{display:block;margin-bottom:7px;font-weight:700;line-height:1.7}.auth-fields input{width:100%;min-width:0;border:2px solid var(--line);border-radius:11px;padding:12px;background:white;color:var(--ink);font-size:18px;min-height:50px;text-align:right}.auth-fields input[dir=ltr]{text-align:left}.auth-fields .wide{grid-column:1/-1}.auth-fields .btn{width:100%}.session-heading{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px}.quiz-meta{font-size:15px;color:var(--muted);line-height:1.8}.quiz-progress{height:7px;background:#e5eae0;border-radius:7px;overflow:hidden;direction:ltr;margin:14px 0}.quiz-progress>div{height:100%;background:var(--green);transition:width .2s}.revealed-answer{background:#fff1ca;border:1px solid #efd18f;border-radius:14px;padding:14px;margin-top:15px;line-height:1.8}.revealed-answer .math{margin:6px 0!important}.result-card{padding:16px;background:#edf4e9;border-radius:15px;margin-top:16px}.result-card .result-number{font-size:42px;font-weight:700;color:var(--green);display:block;direction:ltr;text-align:left}.result-card p{margin:8px 0 12px}.stats-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:18px}.stat-card{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:18px}.stat-card .num{display:block;font-size:30px;font-weight:700;color:var(--green);margin-top:7px}.rank-scroll{overflow-x:auto;max-width:100%;border:1px solid var(--line);border-radius:14px}.rank-table{width:100%;border-collapse:collapse;background:var(--white);font-size:15px}.rank-table th,.rank-table td{padding:13px 12px;border-bottom:1px solid var(--line);text-align:right;line-height:1.7}.rank-table th{background:#e7efe5;font-size:13px;white-space:nowrap}.rank-table .numeric-cell{direction:ltr;text-align:left;font-variant-numeric:tabular-nums;white-space:nowrap}.rank-table tr.self{background:#e3f4e9;font-weight:700}.rank-table tr:last-child td{border-bottom:0}.rank-empty{padding:20px;line-height:1.8;color:var(--muted)}.rank-rules{margin:15px 0;color:var(--muted);font-size:14px;line-height:1.8}.history-list{display:grid;gap:10px;margin-top:14px}.history-row{display:flex;justify-content:space-between;align-items:center;gap:15px;border:1px solid var(--line);background:var(--white);padding:12px 15px;border-radius:12px;line-height:1.8}.history-row small{display:block;color:var(--muted)}.history-score{font-weight:700;font-size:22px;direction:ltr;text-align:left}.network-state{position:fixed;bottom:10px;left:10px;z-index:100;background:var(--ink);color:white;padding:9px 14px;border-radius:24px;font-size:13px;pointer-events:none}.busy button[data-move]{opacity:.55}.table-panel .toolbar{direction:ltr}.table-panel .toolbar>div,.table-panel .toolbar>button{direction:rtl}.draft-note{font-size:12px;color:var(--muted);min-height:18px;margin-top:8px}.start-prompt{padding:22px;border:1px dashed #9fbdab;border-radius:16px;margin-top:16px;line-height:1.8}.section-error{margin-bottom:14px}.quiz-card .word-question{margin:16px 0}.quiz-card .math{margin:18px 0}.quiz-end-actions{display:flex;gap:10px;flex-wrap:wrap}.quiz-end-actions .btn{flex:1}.score-aside{font-size:13px;line-height:1.8;color:var(--muted)}
@media(max-width:480px){.auth-fields{grid-template-columns:1fr;gap:12px}.stats-grid{gap:7px}.stat-card{padding:12px 9px;font-size:12px}.stat-card .num{font-size:24px}.rank-table th,.rank-table td{padding:10px 6px;font-size:12px}.rank-table th{font-size:11px}.rank-table td.name-cell{min-width:82px;word-break:break-word}.auth-tabs{gap:7px}.auth-tabs .btn{font-size:14px;padding:10px 8px}.session-heading{gap:8px}.account-strip{font-size:13px;padding:9px 11px}.quiz-card{padding:15px}.result-card .result-number{font-size:36px}.history-row{font-size:14px;padding:10px}.network-state{font-size:12px;bottom:7px;left:7px}}
    </style>
  </head>
  <body>
    <main class="app" id="app">
      <header>
        <div class="brand-row">
          <div class="brand-mark" aria-hidden="true">×</div>
          <div>
            <div class="brand-name">לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא</div>
            <div class="brand-note">קוֹרְאִים, מְנַסִּים, מַצְלִיחִים.</div>
          </div>
        </div>
        <nav class="nav" aria-label="בְּחִירַת פְּעִילוּת">
          <button data-page="home" class="active" aria-current="page">הַבַּיִת</button>
          <button data-page="table">לוּחַ הַכֶּפֶל</button>
          <button data-page="quick">תִּרְגּוּל מָהִיר</button>
          <button data-page="words">שְׁאֵלוֹת מִלּוּלִיּוֹת</button>
          <button data-page="maze">הַמָּבוֹךְ</button><button data-page="ranking">נִקּוּד וְדֵרוּג</button><button data-page="login" id="nav-login">כְּנִיסַת שַׂחְקָן</button>
        </nav>
<div class="account-strip" id="account-strip"><span id="account-greeting">נִכְנָסִים עִם הַשֵּׁם וְהַקּוֹד, וּמַתְחִילִים לְשַׂחֵק.</span><button class="btn secondary" id="account-action">כְּנִיסָה לַמִּשְׂחָק</button></div>
      </header>
      <div id="global-status" class="status section-error" role="status"></div>
      <section id="page-home" class="page" aria-labelledby="home-title">
        <div class="hero">
          <div>
            <span class="tag">הַהַרְפַּתְקָה שֶׁל שָׁקֵד</span>
            <h1 id="home-title">לוּחַ הַכֶּפֶל שֶׁל<br />שָׁקֵד בֶּן עֶזְרָא</h1>
            <p>
              כָּאן לוֹמְדִים אֶת לוּחַ הַכֶּפֶל עַד <bdi>10</bdi>, בַּדֶּרֶךְ שֶׁהֲכִי אוֹהֲבִים:
              מְמַלְּאִים טַבְלָה, פּוֹתְרִים שְׁאֵלוֹת וְיוֹצְאִים לְהַרְפַּתְקָה בַּיַּעַר. כָּל
              נִסָּיוֹן הוּא הִזְדַּמְּנוּת לִלְמֹד!
            </p>
          </div>
          <div class="hero-art" aria-hidden="true">
            <div class="orb">🌱</div>
            <div class="float one">3 × 4 = 12</div>
            <div class="float two">7 × 8 = 56 ✨</div>
          </div>
        </div>
        <div class="section-kicker">
          <h2>בְּמָה נִרְצֶה לְשַׂחֵק הַיּוֹם?</h2>
          <span>אַרְבַּע דְּרָכִים לְתַרְגֵּל</span>
        </div>
        <div class="activities">
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">▦</span>
              <h3>לוּחַ הַכֶּפֶל</h3>
            </div>
            <p>
              מְמַלְּאִים כַּמָּה תָּאִים שֶׁרוֹצִים וּבוֹדְקִים. תְּשׁוּבָה נְכוֹנָה נִצְבַּעַת
              בְּיָרֹק, וְטָעוּת בְּאָדֹם. הַכֹּל נָכוֹן? חוֹגְגִים עִם זִקּוּקִים!
            </p>
            <button class="btn" data-page="table">
              לַטַּבְלָה <span aria-hidden="true">←</span>
            </button>
          </article>
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">⚡</span>
              <h3>תִּרְגּוּל מָהִיר</h3>
            </div>
            <p>
              תַּרְגִּיל אֶחָד בְּכָל פַּעַם, בְּלִי לַחַץ שֶׁל זְמַן. מַקְלִידִים תְּשׁוּבָה,
              מְקַבְּלִים מָשׁוֹב וְצוֹבְרִים נְקֻדּוֹת.
            </p>
            <button class="btn" data-page="quick">
              לַתִּרְגּוּל <span aria-hidden="true">←</span>
            </button>
          </article>
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">📖</span>
              <h3>שְׁאֵלוֹת מִלּוּלִיּוֹת</h3>
            </div>
            <p>
              מְגַלִּים אֵיפֹה מִסְתַּתֵּר הַכֶּפֶל בְּסִפּוּרִים קְצָרִים מֵחַיֵּי הַיּוֹם־יוֹם.
              קוֹרְאִים, חוֹשְׁבִים וּמַקְלִידִים אֶת הַתְּשׁוּבָה.
            </p>
            <button class="btn" data-page="words">
              לַסִּפּוּרִים <span aria-hidden="true">←</span>
            </button>
          </article>
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">🌲</span>
              <h3>הַמָּבוֹךְ הַקָּסוּם</h3>
            </div>
            <p>
              מִתְקַדְּמִים עִם הַחִצִּים. כָּל שְׁלוֹשָׁה צְעָדִים פּוֹתְרִים שְׁאֵלָה. שָׁלוֹשׁ
              רָמוֹת וּשְׁלוֹשָׁה נִסְיוֹנוֹת לְכָל שְׁאֵלָה!
            </p>
            <button class="btn" data-page="maze">
              לַהַרְפַּתְקָה <span aria-hidden="true">←</span>
            </button>
          </article>
        </div>
      </section>
<section class="page" id="page-login" hidden aria-labelledby="login-title">
 <div class="page-heading"><span class="tag">הַמָּקוֹם שֶׁל כָּל הַכִּתָּה</span><h2 id="login-title">כְּנִיסַת שַׂחְקָן</h2><p>הַשֵּׁם, הַכִּתָּה וְהַקּוֹד מַחְזִירִים אוֹתָנוּ לַהִתְקַדְּמוּת שֶׁלָּנוּ — גַּם מִמַּכְשִׁיר אַחֵר.</p></div>
 <div class="panel auth-panel"><div class="auth-tabs"><button class="btn" id="auth-login" aria-pressed="true">כְּבָר נִרְשַׁמְנוּ</button><button class="btn secondary" id="auth-register" aria-pressed="false">פַּעַם רִאשׁוֹנָה</button></div>
 <form id="auth-form" novalidate><div class="auth-fields">
 <div><label for="auth-first">שֵׁם פְּרָטִי</label><input id="auth-first" name="first_name" maxlength="32" autocomplete="given-name" required></div>
 <div><label for="auth-last">שֵׁם מִשְׁפָּחָה</label><input id="auth-last" name="last_name" maxlength="32" autocomplete="family-name" required></div>
 <div><label for="auth-class">כִּתָּה</label><input id="auth-class" name="class_name" maxlength="24" placeholder="ג׳ 1" autocomplete="off" required></div>
 <div><label for="auth-pin">קוֹד אִישִׁי — אַרְבַּע סְפָרוֹת</label><input id="auth-pin" name="pin" type="password" inputmode="numeric" pattern="[0-9]{4}" minlength="4" maxlength="4" dir="ltr" autocomplete="current-password" required></div>
 <div class="wide"><button class="btn" id="auth-submit" type="submit">נִכְנָסִים לְשַׂחֵק ←</button></div></div></form>
 <div class="status" id="auth-status" role="status"></div><p class="subtle" id="auth-hint" style="margin:14px 0 0">נַקְלִיד אֶת אוֹתָם הַפְּרָטִים שֶׁבָּחַרְנוּ בַּהַרְשָׁמָה.</p></div></section>
 <section class="page" id="page-ranking" hidden aria-labelledby="ranking-title"><div class="page-heading"><span class="tag">כָּל הַצְלָחָה נִסְפֶּרֶת</span><h2 id="ranking-title">הַנִּקּוּד וְהַדֵּרוּג שֶׁלָּנוּ</h2><p id="ranking-class"></p></div>
 <div class="stats-grid"><div class="stat-card">הַמְּמֻצָּע שֶׁלִּי<bdi class="num" id="my-average">—</bdi></div><div class="stat-card">מִשְׂחָקִים שֶׁסֻּיְּמוּ<bdi class="num" id="my-games">0</bdi></div><div class="stat-card">הַמָּקוֹם שֶׁלִּי<bdi class="num" id="my-rank">—</bdi></div></div>
 <div class="toolbar"><h3 style="margin:0">לוּחַ הַכִּתָּה 🏆</h3><button class="btn secondary" id="refresh-ranking">רִעֲנוּן הַדֵּרוּג ↻</button></div>
 <div class="rank-scroll"><table class="rank-table"><thead><tr><th>מָקוֹם</th><th>שֵׁם הַשַּׂחְקָן</th><th>כִּתָּה</th><th>מְמֻצָּע</th><th>מִשְׂחָקִים</th></tr></thead><tbody id="ranking-body"></tbody></table><div id="ranking-empty" class="rank-empty" hidden>עֲדַיִן אֵין תּוֹצָאוֹת. מְסַיְּמִים מִשְׂחָק רִאשׁוֹן וּמַתְחִילִים!</div></div>
 <p class="rank-rules">הַדֵּרוּג הוּא הַמְּמֻצָּע שֶׁל כָּל צִיּוּנֵי הַמִּשְׂחָקִים שֶׁסֻּיְּמוּ, בְּסֻלָּם שֶׁל <bdi>0–100</bdi>. צִיּוּן מִשְׂחָק הוּא אֲחוּז הַתְּשׁוּבוֹת הַנְּכוֹנוֹת בַּנִּסָּיוֹן הָרִאשׁוֹן. בַּטַּבְלָה מְסַיְּמִים אֶת כָּל <bdi>100</bdi> הַתָּאִים. בַּמָּבוֹךְ, שְׁאֵלָה שֶׁהַתְּשׁוּבָה לָהּ נֶחְשְׂפָה אֵינָהּ נִסְפֶּרֶת כִּנְכוֹנָה. הַצִּיּוּן נִשְׁמָר בְּסִיּוּם הָרָמָה. בְּמְמֻצָּע שָׁוֶה מְקַבְּלִים אוֹתוֹ מָקוֹם.</p>
 <h3>הַמִּשְׂחָקִים הָאַחֲרוֹנִים שֶׁלִּי</h3><div id="history-list" class="history-list"></div></section>
      <section id="page-table" class="page" hidden aria-labelledby="table-title">
        <div class="page-heading">
          <span class="tag">מְתַרְגְּלִים בַּקֶּצֶב שֶׁלָּנוּ</span>
          <h2 id="table-title">לוּחַ הַכֶּפֶל</h2>
          <p>
            מְמַלְּאִים גַּם רַק חֵלֶק מֵהַטַּבְלָה, וְאָז לוֹחֲצִים עַל ״בְּדִיקַת תְּשׁוּבוֹת״.
          </p>
        </div>
        <div class="panel table-panel">
          <div class="toolbar">
            <div>
              <div class="subtle">הַתַּרְגִּיל שֶׁבָּחַרְנוּ</div>
              <div class="selected-exercise math" id="selected-exercise" aria-live="polite">
                1 × 1 = ?
              </div>
            </div>
            <button class="btn secondary" id="table-zoom" aria-pressed="false">
              הַגְדָּלַת הַתָּאִים ⤢
            </button>
          </div>
          <p id="zoom-hint" class="subtle" hidden>
            אֶפְשָׁר לְהַחְלִיק אֶת הַטַּבְלָה לַצְּדָדִים.
          </p>
          <div
            class="table-scroll"
            id="table-scroll"
            tabindex="0"
            role="region"
            aria-label="טַבְלַת כֶּפֶל עַד עֶשֶׂר"
          >
            <div
              class="times-table"
              id="times-table"
              role="group"
              aria-label="מִלּוּי לוּחַ הַכֶּפֶל"
            ></div>
          </div>
          <div class="legend">
            <span><i class="dot"></i>נָכוֹן ✓</span
            ><span><i class="dot red"></i>כְּדַאי לְנַסּוֹת שׁוּב ×</span
            ><span><i class="dot neutral"></i>עֲדַיִן לֹא נִבְדַּק</span>
          </div>
          <div class="actions">
            <button class="btn primary" id="check-table">בְּדִיקַת תְּשׁוּבוֹת ✓</button
            ><button class="btn secondary" id="clear-wrong">מְחִיקַת תְּשׁוּבוֹת שְׁגוּיוֹת</button
            ><button class="btn soft" id="clear-table">מְחִיקַת הַכֹּל</button>
          </div>
          <p class="score-aside">אֶפְשָׁר לִבְדֹּק גַּם חֵלֶק מֵהַטַּבְלָה. צִיּוּן לַדֵּרוּג נִשְׁמָר רַק אַחֲרֵי שֶׁמַּשְׁלִימִים אֶת כָּל הַלּוּחַ.</p><div id="table-draft-note" class="draft-note" role="status"></div><div class="status" id="table-status" role="status" aria-live="polite"></div>
        </div>
      </section>
<section class="page" id="page-quick" hidden aria-labelledby="quick-title"><div class="page-heading"><span class="tag">עֶשְׂרִים צְעָדִים שֶׁל הַצְלָחָה</span><h2 id="quick-title">תִּרְגּוּל מָהִיר</h2><p>בְּכָל רָמָה <bdi>20</bdi> שְׁאֵלוֹת. עוֹנִים נָכוֹן וּמַמְשִׁיכִים, בַּקֶּצֶב שֶׁלָּנוּ.</p></div>
    <div class="levels" id="quick-levels"></div><p class="subtle" id="quick-level-note"></p>
    <div class="start-prompt" id="quick-start">בּוֹחֲרִים רָמָה פְּתוּחָה וּמַתְחִילִים סֶבֶב שֶׁל <bdi>20</bdi> שְׁאֵלוֹת.</div>
    <div class="panel quiz-card" id="quick-card" hidden><div class="session-heading"><span class="quiz-meta" id="quick-progress-label"></span><span class="score-pill">נָכוֹן בַּפַּעַם הָרִאשׁוֹנָה <bdi id="quick-first">0</bdi></span></div>
    <div class="quiz-progress"><div id="quick-progress-fill"></div></div><div id="quick-question-area"><div class="math" id="quick-exercise"></div>
    <form class="answer-form" id="quick-form" novalidate><label for="quick-answer">הַתְּשׁוּבָה שֶׁלָּנוּ</label><div class="answer-line"><input id="quick-answer" class="numeric" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="3" dir="ltr" autocomplete="off"><button class="btn" id="quick-submit" type="submit">בְּדִיקָה</button></div></form>
    <div class="status" id="quick-status" role="status"></div><div class="revealed-answer" id="quick-reveal" hidden><strong>נִלְמַד יַחַד אֶת הַתְּשׁוּבָה:</strong><div class="math" id="quick-solution"></div><span>נַקְלִיד אֶת הַתְּשׁוּבָה הַנְּכוֹנָה בַּשָּׂדֶה כְּדֵי לְהַמְשִׁיךְ.</span></div>
    <div class="actions"><button class="btn secondary" id="quick-next" disabled>לַשְּׁאֵלָה הַבָּאָה ←</button></div></div><div id="quick-result" class="result-card" hidden></div></div>
    <p class="rank-rules">כְּדֵי לִפְתֹּחַ אֶת הָרָמָה הַבָּאָה צָרִיךְ לַעֲנוֹת נָכוֹן בַּנִּסָּיוֹן הָרִאשׁוֹן עַל לְפָחוֹת <bdi>16 / 20</bdi> שְׁאֵלוֹת (<bdi>80%</bdi>). אַחֲרֵי שָׁלוֹשׁ טָעֻיּוֹת תּוּצַג הַתְּשׁוּבָה. תִּקּוּן מְאַפְשֵׁר לְהַמְשִׁיךְ, אֲבָל אֵינוֹ מְשַׁנֶּה אֶת צִיּוּן הַנִּסָּיוֹן הָרִאשׁוֹן.</p></section><section class="page" id="page-words" hidden aria-labelledby="words-title"><div class="page-heading"><span class="tag">מָאתַיִם סִפּוּרִים, שָׁלוֹשׁ רָמוֹת</span><h2 id="words-title">שְׁאֵלוֹת מִלּוּלִיּוֹת</h2><p>בְּכָל רָמָה <bdi>20</bdi> שְׁאֵלוֹת. עוֹנִים נָכוֹן וּמַמְשִׁיכִים, בַּקֶּצֶב שֶׁלָּנוּ.</p></div>
    <div class="levels" id="words-levels"></div><p class="subtle" id="words-level-note"></p>
    <div class="start-prompt" id="words-start">בּוֹחֲרִים רָמָה פְּתוּחָה וּמַתְחִילִים סֶבֶב שֶׁל <bdi>20</bdi> שְׁאֵלוֹת.</div>
    <div class="panel quiz-card" id="words-card" hidden><div class="session-heading"><span class="quiz-meta" id="words-progress-label"></span><span class="score-pill">נָכוֹן בַּפַּעַם הָרִאשׁוֹנָה <bdi id="words-first">0</bdi></span></div>
    <div class="quiz-progress"><div id="words-progress-fill"></div></div><div id="words-question-area"><p class="word-question" id="words-question"></p>
    <form class="answer-form" id="words-form" novalidate><label for="words-answer">הַתְּשׁוּבָה שֶׁלָּנוּ</label><div class="answer-line"><input id="words-answer" class="numeric" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="3" dir="ltr" autocomplete="off"><button class="btn" id="words-submit" type="submit">בְּדִיקָה</button></div></form>
    <div class="status" id="words-status" role="status"></div><div class="revealed-answer" id="words-reveal" hidden><strong>נִלְמַד יַחַד אֶת הַתְּשׁוּבָה:</strong><div class="math" id="words-solution"></div><span>נַקְלִיד אֶת הַתְּשׁוּבָה הַנְּכוֹנָה בַּשָּׂדֶה כְּדֵי לְהַמְשִׁיךְ.</span></div>
    <div class="actions"><button class="btn secondary" id="words-next" disabled>לַשְּׁאֵלָה הַבָּאָה ←</button></div></div><div id="words-result" class="result-card" hidden></div></div>
    <p class="rank-rules">כְּדֵי לִפְתֹּחַ אֶת הָרָמָה הַבָּאָה צָרִיךְ לַעֲנוֹת נָכוֹן בַּנִּסָּיוֹן הָרִאשׁוֹן עַל לְפָחוֹת <bdi>16 / 20</bdi> שְׁאֵלוֹת (<bdi>80%</bdi>). אַחֲרֵי שָׁלוֹשׁ טָעֻיּוֹת תּוּצַג הַתְּשׁוּבָה. תִּקּוּן מְאַפְשֵׁר לְהַמְשִׁיךְ, אֲבָל אֵינוֹ מְשַׁנֶּה אֶת צִיּוּן הַנִּסָּיוֹן הָרִאשׁוֹן.</p></section>      <section id="page-maze" class="page" hidden aria-labelledby="maze-title">
        <div class="page-heading">
          <span class="tag">הַרְפַּתְקָה בֵּין הָעֵצִים</span>
          <h2 id="maze-title">הַמָּבוֹךְ הַקָּסוּם</h2>
          <p>כָּל שְׁלוֹשָׁה צְעָדִים — שְׁאֵלַת כֶּפֶל. פּוֹתְרִים וּמַמְשִׁיכִים לַדֶּגֶל!</p>
        </div>
        <div class="levels" id="levels" aria-label="רָמוֹת הַמִּשְׂחָק"></div>
        <div class="start-prompt" id="maze-start">בּוֹחֲרִים רָמָה וְיוֹצְאִים לַהַרְפַּתְקָה!</div><div class="panel maze-panel" id="maze-panel" hidden>
          <div class="maze-stats">
            <span id="maze-stage"></span
            ><span class="hearts" id="maze-hearts" aria-live="polite"></span
            ><span class="score-pill">⭐ <bdi id="maze-score">0</bdi></span>
          </div>
          <div
            class="progress-track"
            role="progressbar"
            id="maze-progress"
            aria-label="הִתְקַדְּמוּת בָּרָמָה"
            aria-valuemin="0"
            aria-valuemax="10"
            aria-valuenow="0"
          >
            <div class="progress-fill" id="maze-progress-fill"></div>
          </div>
          <div class="maze-layout">
            <div>
              <div class="maze-arena" id="maze-arena">
                <div
                  class="maze-board"
                  id="maze-board"
                  role="img"
                  aria-label="מַפַּת הַמָּבוֹךְ"
                ></div>
                <div
                  class="maze-overlay"
                  id="maze-question"
                  hidden
                  role="dialog"
                  aria-labelledby="maze-question-title"
                >
                  <div class="question-box">
                    <h3 id="maze-question-title">עֲצִירָה לְשְׁאֵלָה ✨</h3>
                    <div class="math" id="maze-exercise"></div>
                    <form id="maze-form" novalidate>
                      <label for="maze-answer">מַקְלִידִים אֶת הַתְּשׁוּבָה</label>
                      <div class="answer-line">
                        <input
                          id="maze-answer"
                          class="numeric"
                          type="text"
                          inputmode="numeric"
                          pattern="[0-9]*"
                          maxlength="3"
                          dir="ltr"
                          autocomplete="off"
                        /><button class="btn" type="submit">בְּדִיקָה</button>
                      </div>
                    </form>
                    <div id="maze-answer-status" class="status" role="status"></div>
                    <div id="maze-reveal" hidden><p class="subtle" style="margin:8px 0 12px">מַמְשִׁיכִים לַהַרְפַּתְקָה! הַשְּׁאֵלָה הַזֹּאת לֹא מוֹסִיפָה נְקֻדּוֹת.</p><button class="btn" id="maze-continue" type="button">מַמְשִׁיכִים ←</button></div>
                  </div>
                </div>
                <div class="maze-overlay" id="maze-end" hidden>
                  <div class="question-box end-box" id="maze-end-content" role="status"></div>
                </div>
              </div>
              <div class="maze-caption" id="maze-caption"></div>
            </div>
            <div class="controls-panel">
              <strong>לְאָן מִתְקַדְּמִים?</strong>
              <div class="dpad" aria-label="כַּפְתּוֹרֵי תְּנוּעָה">
                <button data-move="up" aria-label="לְמַעְלָה">↑</button
                ><button data-move="left" aria-label="שְׂמֹאלָה">←</button
                ><span class="dpad-center" aria-hidden="true">✥</span
                ><button data-move="right" aria-label="יָמִינָה">→</button
                ><button data-move="down" aria-label="לְמַטָּה">↓</button>
              </div>
              <div class="status" id="maze-status" role="status"></div>
              <p class="subtle">
                בְּכָל שְׁאֵלָה יֵשׁ שְׁלוֹשָׁה לְבָבוֹת. עוֹנִים נָכוֹן כְּדֵי לְהַמְשִׁיךְ. אַחֲרֵי שָׁלוֹשׁ טָעֻיּוֹת רוֹאִים אֶת הַתְּשׁוּבָה וְלוֹחֲצִים ״מַמְשִׁיכִים״, לְלֹא נִקּוּד לַשְּׁאֵלָה.
              </p>
              <button class="btn soft" id="maze-restart">הַתְחָלַת הָרָמָה מֵחָדָשׁ ↻</button>
            </div>
          </div>
        </div>
        <p class="subtle" style="margin-top: 14px">
          כְּדֵי לִפְתֹּחַ אֶת הָרָמָה הַבָּאָה, מְסַיְּמִים אֶת הָרָמָה עִם לְפָחוֹת
          <bdi>80%</bdi> תְּשׁוּבוֹת נְכוֹנוֹת בַּנִּסָּיוֹן הָרִאשׁוֹן. כָּל תְּשׁוּבָה נְכוֹנָה
          מְזַכָּה בִּנְקֻדּוֹת.
        </p>
      </section>
<footer class="footer">נִבְנָה בְּאַהֲבָה לְשָׁקֵד וּלְחַבְרֵי הַכִּתָּה · הַתּוֹצָאוֹת וְהַהִתְקַדְּמוּת נִשְׁמָרוֹת בַּחֶשְׁבּוֹן הָאִישִׁי.</footer>
    </main>
    <div class="fireworks" id="fireworks" aria-hidden="true"></div>
<div id="network-state" class="network-state" hidden role="status">שׁוֹמְרִים וּמְעַדְכְּנִים…</div>
<script>
"use strict";
const $ = (id) => document.getElementById(id);
const LEVEL_NAMES = ["א׳", "ב׳", "ג׳"];
const GAME_NAMES = {
  quick: "תִּרְגּוּל מָהִיר",
  words: "שְׁאֵלוֹת מִלּוּלִיּוֹת",
  maze: "הַמָּבוֹךְ",
  table: "לוּחַ הַכֶּפֶל",
};
let snapshot = null,
  configured = false,
  ready = false,
  page = "home",
  afterLogin = "home",
  authMode = "login";
let pending = null,
  lastReply = null,
  lastHeight = 0,
  heightQueued = false,
  queue = [],
  fireworkTimer = null;
let tableDraft = Array(100).fill(""),
  draftRun = null,
  dirty = false,
  draftVersion = 0,
  saveTimer = null,
  large = false;
let questionKeys = {},
  lastMazePending = false,
  restartConfirm = false;
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c],
  );
const n = (value) => "<bdi>" + esc(value) + "</bdi>";
const fixed = (value) =>
  value === null || value === undefined
    ? "—"
    : Number(value).toLocaleString("he-IL", { maximumFractionDigits: 2 });
const uid = () =>
  globalThis.crypto?.randomUUID?.() ||
  "r_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2);
const normalizeDigits = (value) =>
  value
    .replace(/[٠-٩]/g, (c) => String(c.charCodeAt(0) - 1632))
    .replace(/[۰-۹]/g, (c) => String(c.charCodeAt(0) - 1776));
document.addEventListener(
  "input",
  (event) => {
    if (event.target.matches("input[inputmode=numeric]"))
      event.target.value = normalizeDigits(event.target.value);
  },
  true,
);

function message(type, extra = {}) {
  if (window.parent !== window)
    window.parent.postMessage({ isStreamlitMessage: true, type, ...extra }, "*");
}
function resizeFrame() {
  if (heightQueued) return;
  heightQueued = true;
  requestAnimationFrame(() => {
    heightQueued = false;
    const height = Math.ceil($("app").getBoundingClientRect().height) + 4;
    if (height !== lastHeight) {
      lastHeight = height;
      message("streamlit:setFrameHeight", { height });
    }
  });
}
function status(id, text, kind = "") {
  const el = $(id);
  if (!el) return;
  el.textContent = text;
  el.className = "status " + kind;
  resizeFrame();
}
function rpc(action, payload = {}) {
  return new Promise((resolve, reject) => {
    queue.push({ id: uid(), action, payload, resolve, reject, retries: 0 });
    pump();
  });
}
function pump() {
  if (pending || !queue.length) return;
  pending = queue.shift();
  setBusy(true);
  sendPending();
}
function sendPending() {
  const p = pending;
  if (!p) return;
  message("streamlit:setComponentValue", {
    dataType: "json",
    value: { id: p.id, action: p.action, payload: p.payload, nonce: uid() },
  });
  clearTimeout(p.timer);
  p.timer = setTimeout(() => {
    if (!pending || pending.id !== p.id) return;
    if (p.retries++ < 1) {
      sendPending();
      return;
    }
    pending = null;
    p.reject(new Error("הַחִבּוּר אִטִּי. נִרְעֲנֵן כְּדֵי לִבְדֹּק אִם הַפְּעֻלָּה נִשְׁמְרָה."));
    setBusy(false);
    pump();
  }, 18000);
}
function setBusy(busy) {
  $("network-state").hidden = !busy;
  document.body.classList.toggle("busy", busy);
  document.querySelectorAll("[data-server]").forEach((el) => {
    el.disabled = busy || el.dataset.locked === "true";
  });
}
function serverButton(button, locked = false) {
  button.dataset.server = "true";
  button.dataset.locked = String(locked);
  button.disabled = !!pending || locked;
}
function actionError(error, target = "global-status") {
  status(target, error.message || "הַפְּעֻלָּה לֹא הֻשְׁלְמָה. נְנַסֶּה שׁוּב.", "error");
}
window.addEventListener("message", (event) => {
  if (event.source !== window.parent || event.data?.type !== "streamlit:render") return;
  const args = event.data.args || {};
  configured = !!args.configured;
  ready = true;
  const reply = args.response;
  if (reply && reply.id !== lastReply) {
    lastReply = reply.id;
    if (Object.hasOwn(reply, "snapshot")) snapshot = reply.snapshot;
    const current = pending && pending.id === reply.id ? pending : null;
    if (current) {
      clearTimeout(current.timer);
      pending = null;
    }
    renderAll();
    if (reply.ok && reply.celebrate) fireworks();
    if (current) {
      current.payload = null;
      if (reply.ok) current.resolve(reply);
      else current.reject(new Error(reply.error));
    }
    setBusy(false);
    pump();
  } else if (!lastReply) {
    snapshot = args.snapshot || null;
    renderAll();
  }
  resizeFrame();
});
function navigate(next) {
  if (!["home", "login", "ranking", "table", "quick", "words", "maze"].includes(next)) return;
  if (!snapshot && !["home", "login"].includes(next)) {
    afterLogin = next;
    next = "login";
  }
  if (page === "table" && next !== "table" && dirty) flushTable().catch(actionError);
  page = next;
  document.querySelectorAll(".page").forEach((el) => (el.hidden = el.id !== "page-" + page));
  document.querySelectorAll(".nav [data-page]").forEach((button) => {
    const on = button.dataset.page === page;
    button.classList.toggle("active", on);
    if (on) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
  status("global-status", "");
  renderAll();
  if (page === "ranking" && snapshot) rpc("sync").catch(actionError);
  $("app").scrollIntoView({ block: "start", behavior: "instant" });
  resizeFrame();
}
document
  .querySelectorAll("[data-page]")
  .forEach((button) => button.addEventListener("click", () => navigate(button.dataset.page)));
function renderAll() {
  const user = snapshot?.player;
  $("nav-login").hidden = !!user;
  $("account-greeting").textContent = user
    ? `${user.first_name} ${user.last_name} · כִּתָּה ${user.class_name}`
    : "נִכְנָסִים עִם הַשֵּׁם וְהַקּוֹד, וּמַתְחִילִים לְשַׂחֵק.";
  $("account-action").textContent = user ? "הַחְלָפַת שַׂחְקָן" : "כְּנִיסָה לַמִּשְׂחָק";
  serverButton($("auth-submit"), !ready || !configured);
  if (ready && !configured)
    status("auth-status", "הַמֶּרְחָב הַכִּתָּתִי בַּהֲכָנָה. הַכְּנִיסָה תִּפָּתַח בְּקָרוֹב.");
  if (user) {
    renderTable();
    renderQuiz("quick");
    renderQuiz("words");
    renderMaze();
    renderRanking();
  }
  resizeFrame();
}
function setAuthMode(mode) {
  authMode = mode;
  for (const name of ["login", "register"]) {
    const on = name === mode;
    const b = $("auth-" + name);
    b.className = "btn" + (on ? "" : " secondary");
    b.setAttribute("aria-pressed", String(on));
  }
  $("auth-submit").textContent =
    mode === "register" ? "נִרְשָׁמִים וּמַתְחִילִים ←" : "נִכְנָסִים לְשַׂחֵק ←";
  $("auth-pin").autocomplete = mode === "register" ? "new-password" : "current-password";
  $("auth-hint").textContent =
    mode === "register"
      ? "בּוֹחֲרִים קוֹד שֶׁנּוּכַל לִזְכֹּר. הַקּוֹד אֵינוֹ מֻצָּג בַּדֵּרוּג."
      : "נַקְלִיד אֶת אוֹתָם הַפְּרָטִים שֶׁבָּחַרְנוּ בַּהַרְשָׁמָה.";
  status("auth-status", "");
}
$("auth-login").addEventListener("click", () => setAuthMode("login"));
$("auth-register").addEventListener("click", () => setAuthMode("register"));
$("auth-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!configured || pending) return;
  const data = {
    first: $("auth-first").value.trim(),
    last: $("auth-last").value.trim(),
    class_name: $("auth-class").value.trim(),
    pin: $("auth-pin").value,
  };
  if (!data.first || !data.last || !data.class_name || !/^\d{4}$/.test(data.pin)) {
    status(
      "auth-status",
      "נְמַלֵּא שֵׁם, שֵׁם מִשְׁפָּחָה, כִּתָּה וְקוֹד בֶּן אַרְבַּע סְפָרוֹת.",
      "warning",
    );
    return;
  }
  try {
    await rpc(authMode, data);
    $("auth-pin").value = "";
    questionKeys = {};
    dirty = false;
    draftRun = null;
    status("auth-status", "");
    navigate(afterLogin);
    rpc("sync").catch(actionError);
  } catch (error) {
    actionError(error, "auth-status");
    $("auth-pin").select();
  }
});
$("account-action").addEventListener("click", async () => {
  if (!snapshot) {
    navigate("login");
    return;
  }
  try {
    if (dirty) await flushTable();
    await rpc("logout");
    clearTimeout(saveTimer);
    dirty = false;
    draftRun = null;
    tableDraft = Array(100).fill("");
    questionKeys = {};
    $("auth-pin").value = "";
    $("auth-first").value = "";
    $("auth-last").value = "";
    $("auth-class").value = "";
    afterLogin = "home";
    navigate("login");
  } catch (error) {
    actionError(error);
  }
});

function fireworks() {
  clearTimeout(fireworkTimer);
  const layer = $("fireworks");
  layer.replaceChildren();
  const colors = ["#1b947a", "#ffbf45", "#e9798c", "#8872c4", "#45a6cd"];
  for (let burst = 0; burst < 7; burst++) {
    const x = 12 + Math.random() * 76,
      y = 10 + Math.random() * 50;
    for (let i = 0; i < 22; i++) {
      const spark = document.createElement("i");
      spark.className = "spark";
      const angle = (i / 22) * Math.PI * 2,
        distance = 35 + Math.random() * 100;
      spark.style.cssText = `left:${x}%;top:${y}%;--spark:${colors[(i + burst) % colors.length]};--dx:${Math.cos(angle) * distance}px;--dy:${Math.sin(angle) * distance + 35}px;--delay:${burst * 0.24}s`;
      layer.append(spark);
    }
  }
  fireworkTimer = setTimeout(() => layer.replaceChildren(), 2900);
}

// Preserve the spreadsheet geometry. Drafts belong to the signed-in player only.
function createTable() {
  const frag = document.createDocumentFragment();
  for (let r = 0; r <= 10; r++)
    for (let c = 0; c <= 10; c++) {
      const cell = document.createElement("div");
      cell.className = "table-cell";
      if (!r || !c) {
        cell.classList.add("head");
        if (!r && !c) cell.classList.add("corner");
        cell.textContent = !r && !c ? "×" : String(r || c);
        cell.setAttribute("aria-hidden", "true");
      } else {
        const i = (r - 1) * 10 + c - 1;
        cell.id = "cell-" + i;
        const input = document.createElement("input");
        input.type = "text";
        input.inputMode = "numeric";
        input.pattern = "[0-9]*";
        input.maxLength = 3;
        input.autocomplete = "off";
        input.dir = "ltr";
        input.id = "table-" + i;
        input.setAttribute("aria-label", `${r} כָּפוּל ${c}`);
        input.addEventListener("focus", () => {
          $("selected-exercise").textContent = `${r} × ${c} = ?`;
        });
        input.addEventListener("input", () => {
          tableDraft[i] = input.value;
          dirty = true;
          draftVersion++;
          cell.className = "table-cell";
          input.setAttribute("aria-invalid", "false");
          $("table-draft-note").textContent = "מַמְתִּינִים לִשְׁמִירָה…";
          status("table-status", "");
          clearTimeout(saveTimer);
          saveTimer = setTimeout(() => flushTable().catch(actionError), 700);
        });
        input.addEventListener("keydown", (event) => {
          const delta = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -10, ArrowDown: 10, Enter: 1 }[
            event.key
          ];
          if (delta !== undefined && i + delta >= 0 && i + delta < 100) {
            event.preventDefault();
            $("table-" + (i + delta)).focus();
            $("table-" + (i + delta)).select();
          }
        });
        cell.append(input);
      }
      frag.append(cell);
    }
  $("times-table").replaceChildren(frag);
}
function renderTable() {
  const t = snapshot.runs.table;
  if ((t?.id || null) !== draftRun) {
    const preserve = dirty && draftRun === null && !!t;
    if (!preserve) {
      tableDraft = t ? [...t.values] : Array(100).fill("");
      dirty = false;
      draftVersion++;
    }
    draftRun = t?.id || null;
  } else if (!dirty && t) tableDraft = [...t.values];
  tableDraft.forEach((value, i) => {
    const input = $("table-" + i);
    if (document.activeElement !== input && input.value !== value) input.value = value;
    input.disabled = !!t && t.status !== "active";
    const mark = t && value === t.values[i] ? t.marks[i] : "";
    $("cell-" + i).className = "table-cell" + (mark ? " " + mark : "");
    input.setAttribute("aria-invalid", String(mark === "wrong"));
  });
  $("times-table").classList.toggle("large", large);
  $("table-zoom").setAttribute("aria-pressed", String(large));
  $("table-zoom").textContent = large ? "כָּל הַלּוּחַ בַּמָּסָךְ ⤡" : "הַגְדָּלַת הַתָּאִים ⤢";
  $("zoom-hint").hidden = !large;
  serverButton($("check-table"), !!t && t.status !== "active");
  serverButton($("clear-wrong"), !!t && t.status !== "active");
  serverButton($("clear-table"));
  if (t && t.status !== "active")
    status(
      "table-status",
      `הַלּוּחַ הֻשְׁלַם! הַצִּיּוּן ${fixed(t.score)} נִשְׁמַר בַּדֵּרוּג. לְלוּחַ חָדָשׁ לוֹחֲצִים עַל מְחִיקַת הַכֹּל.`,
      "success",
    );
}
async function tableAction(action) {
  clearTimeout(saveTimer);
  if (!snapshot) return;
  const version = draftVersion,
    values = [...tableDraft],
    run_id = draftRun;
  try {
    const reply = await rpc(action, { run_id, values });
    if (version === draftVersion) {
      dirty = false;
      renderTable();
      $("table-draft-note").textContent = "הַשִּׁנּוּיִים נִשְׁמְרוּ ✓";
    }
    if (action === "table_check" && snapshot.runs.table?.status === "active") {
      const marks = snapshot.runs.table.marks,
        correct = marks.filter((x) => x === "correct").length,
        wrong = marks.filter((x) => x === "wrong").length;
      status(
        "table-status",
        correct + wrong
          ? `${correct} תְּשׁוּבוֹת נְכוֹנוֹת מִתּוֹךְ ${correct + wrong}. ${wrong ? "אֶפְשָׁר לְתַקֵּן וְלִבְדֹּק שׁוּב." : "כָּל הַכָּבוֹד! 🎆"}`
          : "עֲדַיִן לֹא מִלֵּאנוּ תְּשׁוּבוֹת.",
        wrong ? "warning" : correct ? "success" : "",
      );
    }
    return reply;
  } catch (error) {
    $("table-draft-note").textContent = "הַשִּׁנּוּיִים עֲדַיִן לֹא נִשְׁמְרוּ.";
    throw error;
  }
}
function flushTable() {
  return dirty ? tableAction("table_save") : Promise.resolve();
}
$("check-table").addEventListener("click", () =>
  tableAction("table_check").catch((error) => actionError(error, "table-status")),
);
$("clear-wrong").addEventListener("click", () =>
  tableAction("table_clear_wrong").catch((error) => actionError(error, "table-status")),
);
$("clear-table").addEventListener("click", async () => {
  clearTimeout(saveTimer);
  dirty = false;
  draftVersion++;
  try {
    await rpc("table_clear", { run_id: draftRun });
    status("table-status", "הַטַּבְלָה נְקִיָּה. מַתְחִילִים מֵחָדָשׁ!");
  } catch (error) {
    actionError(error, "table-status");
  }
});
$("table-zoom").addEventListener("click", () => {
  large = !large;
  renderTable();
  resizeFrame();
});

function levels(activity, id) {
  const container = $(id),
    run = snapshot.runs[activity],
    opened = snapshot.unlocked[activity];
  container.replaceChildren();
  for (let level = 0; level < 3; level++) {
    const button = document.createElement("button"),
      locked = level > opened || (run?.status === "active" && run.level !== level);
    button.className = "level" + (run?.level === level ? " active" : "");
    button.dataset.level = level;
    button.dataset.activity = activity;
    button.setAttribute("aria-pressed", String(run?.level === level));
    const total = activity === "maze" ? [10, 15, 20][level] : 20;
    button.innerHTML = `<strong>${level > opened ? "🔒 " : ""}רָמָה ${LEVEL_NAMES[level]}</strong><small>${n(total)} ${activity === "maze" ? "שְׁלָבִים" : "שְׁאֵלוֹת"}</small>`;
    serverButton(button, locked);
    button.addEventListener("click", () => rpc("start", { activity, level }).catch(actionError));
    container.append(button);
  }
}
function renderQuiz(activity) {
  const run = snapshot.runs[activity];
  levels(activity, activity + "-levels");
  $(activity + "-start").hidden = !!run;
  $(activity + "-card").hidden = !run;
  $(activity + "-level-note").textContent =
    run?.status === "active"
      ? "הַסֶּבֶב הַנּוֹכְחִי נִשְׁמָר. מְסַיְּמִים אוֹתוֹ לִפְנֵי שֶׁמַּתְחִילִים סֶבֶב אַחֵר."
      : activity === "words"
        ? "בְּכָל נִסָּיוֹן מֻגְרָלוֹת שְׁאֵלוֹת מַתְאִימוֹת לָרָמָה מִמַּאֲגָר שֶׁל 200 שְׁאֵלוֹת."
        : "";
  if (!run) return;
  $(activity + "-progress-label").innerHTML =
    `רָמָה ${LEVEL_NAMES[run.level]} · שְׁאֵלָה ${n(Math.min(run.index + 1, 20) + " / 20")}`;
  $(activity + "-first").textContent = run.first_correct;
  $(activity + "-progress-fill").style.width = (run.completed / 20) * 100 + "%";
  const ended = run.status !== "active";
  $(activity + "-question-area").hidden = ended;
  $(activity + "-result").hidden = !ended;
  if (ended) {
    renderQuizResult(activity, run);
    return;
  }
  const q = run.question,
    input = $(activity + "-answer");
  if (questionKeys[activity] !== q.key) {
    questionKeys[activity] = q.key;
    input.value = "";
  }
  if (activity === "quick") $("quick-exercise").textContent = `${q.a} × ${q.b} = ?`;
  else $("words-question").innerHTML = esc(q.text).replace(/\d+/g, (x) => n(x));
  input.disabled = run.solved;
  serverButton($(activity + "-submit"), run.solved);
  serverButton($(activity + "-next"), !run.solved);
  $(activity + "-reveal").hidden = !run.revealed;
  if (run.revealed)
    $(activity + "-solution").textContent =
      activity === "quick" ? `${q.a} × ${q.b} = ${q.answer}` : String(q.answer);
  status(
    activity + "-status",
    run.solved
      ? "נָכוֹן! עַכְשָׁו אֶפְשָׁר לְהַמְשִׁיךְ."
      : run.tries
        ? `נְנַסֶּה שׁוּב. נִסְיוֹנוֹת שֶׁלֹּא הִצְלִיחוּ: ${run.tries}.`
        : "",
    run.solved ? "success" : run.tries ? "warning" : "",
  );
}
function renderQuizResult(activity, run) {
  const node = $(activity + "-result");
  node.replaceChildren();
  const title = document.createElement("h3");
  title.textContent =
    run.status === "passed"
      ? "כָּל הַכָּבוֹד! עָבַרְנוּ אֶת הָרָמָה 🏆"
      : "סִיַּמְנוּ סֶבֶב שֶׁל לְמִידָה 🌱";
  const value = document.createElement("bdi");
  value.className = "result-number";
  value.textContent = fixed(run.score) + " / 100";
  const text = document.createElement("p");
  text.innerHTML = `${n(run.first_correct + " / 20")} תְּשׁוּבוֹת נְכוֹנוֹת בַּנִּסָּיוֹן הָרִאשׁוֹן. הַצִּיּוּן נִכְלַל בַּמְּמֻצָּע.${run.status === "passed" ? "" : " נְנַסֶּה שׁוּב כְּדֵי לְהַגִּיעַ לְ־" + n("80%") + "."}`;
  const actions = document.createElement("div");
  actions.className = "quiz-end-actions";
  if (run.status === "passed" && run.level < 2) {
    const next = document.createElement("button");
    next.className = "btn";
    next.textContent = "לָרָמָה הַבָּאָה ←";
    serverButton(next);
    next.addEventListener("click", () =>
      rpc("start", { activity, level: run.level + 1 }).catch(actionError),
    );
    actions.append(next);
  }
  const again = document.createElement("button");
  again.className = "btn secondary";
  again.textContent = "הַגְרָלָה חֲדָשָׁה בְּאוֹתָהּ רָמָה";
  serverButton(again);
  again.addEventListener("click", () =>
    rpc("start", { activity, level: run.level }).catch(actionError),
  );
  actions.append(again);
  node.append(title, value, text, actions);
}
for (const activity of ["quick", "words"]) {
  $(activity + "-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const run = snapshot?.runs[activity];
    if (!run || run.solved || pending) return;
    try {
      await rpc("answer", {
        run_id: run.id,
        question_key: run.question.key,
        answer: $(activity + "-answer").value,
      });
      const current = snapshot.runs[activity];
      if (current.revealed && current.tries === 3 && !current.solved) {
        $(activity + "-answer").blur();
        $(activity + "-reveal").scrollIntoView({ block: "center", behavior: "instant" });
      } else if (!current.solved) $(activity + "-answer").select();
    } catch (error) {
      actionError(error, activity + "-status");
    }
  });
  $(activity + "-next").addEventListener("click", () => {
    const run = snapshot?.runs[activity];
    if (run?.solved)
      rpc("next", { run_id: run.id, question_key: run.question.key }).catch((error) =>
        actionError(error, activity + "-status"),
      );
  });
}

function renderMaze() {
  levels("maze", "levels");
  const m = snapshot.runs.maze;
  $("maze-start").hidden = !!m;
  $("maze-panel").hidden = !m;
  if (!m) return;
  $("maze-stage").innerHTML =
    `רָמָה ${LEVEL_NAMES[m.level]} · שָׁלָב ${n(Math.min(m.completed + 1, m.total) + " / " + m.total)}`;
  $("maze-hearts").textContent = "❤️".repeat(m.lives) + "🤍".repeat(3 - m.lives);
  $("maze-hearts").setAttribute("aria-label", `נוֹתְרוּ ${m.lives} לְבָבוֹת`);
  $("maze-score").textContent = m.points;
  $("maze-progress").setAttribute("aria-valuemax", m.total);
  $("maze-progress").setAttribute("aria-valuenow", m.completed);
  $("maze-progress-fill").style.width = (m.completed / m.total) * 100 + "%";
  const board = $("maze-board");
  board.replaceChildren();
  for (let y = 0; y < 9; y++)
    for (let x = 0; x < 9; x++) {
      const cell = document.createElement("div");
      cell.className = "maze-cell";
      cell.dataset.x = x;
      cell.dataset.y = y;
      if (m.grid[y][x]) cell.classList.add("wall");
      if (m.visited[y * 9 + x]) cell.classList.add("visited");
      if (x === m.goal.x && y === m.goal.y) {
        cell.classList.add("goal");
        cell.textContent = "🚩";
      }
      if (x === m.x && y === m.y) {
        cell.classList.add("player");
        cell.textContent = "🧒";
      }
      board.append(cell);
    }
  board.setAttribute("aria-label", `מַפַּת הַמָּבוֹךְ. שׁוּרָה ${m.y}, עַמּוּדָה ${m.x}.`);
  $("maze-caption").innerHTML =
    m.completed >= m.total
      ? "סִיַּמְנוּ אֶת כָּל הַשְּׁאֵלוֹת. מַגִּיעִים לַדֶּגֶל!"
      : `צְעָדִים עַד לַשְּׁאֵלָה הַבָּאָה: ${n(3 - m.moves)}`;
  $("maze-question").hidden = !m.pending || m.status !== "active";
  $("maze-end").hidden = m.status === "active";
  document
    .querySelectorAll("[data-move]")
    .forEach((button) => serverButton(button, m.pending || m.status !== "active"));
  serverButton($("maze-restart"));
  $("maze-restart").textContent = restartConfirm
    ? "לְהַתְחִיל מֵחָדָשׁ? לְחִיצָה נוֹסֶפֶת לְאִשּׁוּר"
    : "הַתְחָלַת הָרָמָה מֵחָדָשׁ ↻";
  if (m.pending) {
    const q = m.question;
    $("maze-question-title").textContent = m.revealed
      ? "נִלְמַד יַחַד אֶת הַתְּשׁוּבָה ✨"
      : "עֲצִירָה לְשְׁאֵלָה ✨";
    $("maze-exercise").textContent = `${q.a} × ${q.b} = ${m.revealed ? q.answer : "?"}`;
    $("maze-form").hidden = m.revealed;
    $("maze-reveal").hidden = !m.revealed;
    if (questionKeys.maze !== q.key) {
      $("maze-answer").value = "";
      questionKeys.maze = q.key;
    }
    serverButton($("maze-form").querySelector("button"), m.revealed);
    serverButton($("maze-continue"), !m.revealed);
    status(
      "maze-answer-status",
      m.tries && !m.revealed ? `נְנַסֶּה שׁוּב. נוֹתְרוּ ${m.lives} לְבָבוֹת.` : "",
      m.tries && !m.revealed ? "error" : "",
    );
    if (!lastMazePending && page === "maze") {
      requestAnimationFrame(() => {
        $("maze-question").scrollIntoView({ block: "center", behavior: "instant" });
        $(m.revealed ? "maze-continue" : "maze-answer").focus({ preventScroll: true });
      });
    }
  }
  lastMazePending = m.pending;
  if (m.status !== "active") renderMazeEnd(m);
}
function move(direction) {
  const m = snapshot?.runs.maze;
  if (page !== "maze" || !m || pending || m.pending || m.status !== "active") return;
  const [dx, dy] = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[direction];
  if (m.grid[m.y + dy]?.[m.x + dx] !== 0) {
    status("maze-status", "כָּאן יֵשׁ עֵץ. נִבְחַר כִּוּוּן אַחֵר.");
    return;
  }
  restartConfirm = false;
  status("maze-status", "");
  rpc("move", { run_id: m.id, direction }).catch((error) => actionError(error, "maze-status"));
}
document
  .querySelectorAll("[data-move]")
  .forEach((button) => button.addEventListener("click", () => move(button.dataset.move)));
document.addEventListener("keydown", (event) => {
  if (event.target.matches("input,textarea") || event.altKey || event.ctrlKey || event.metaKey)
    return;
  const direction = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right" }[
    event.key
  ];
  if (page === "maze" && direction) {
    event.preventDefault();
    move(direction);
  }
});
$("maze-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const m = snapshot?.runs.maze;
  if (!m?.pending || m.revealed || pending) return;
  try {
    await rpc("answer", {
      run_id: m.id,
      question_key: m.question.key,
      answer: $("maze-answer").value,
    });
    if (snapshot.runs.maze.pending && !snapshot.runs.maze.revealed)
      $("maze-answer").select();
    else {
      $("maze-answer").blur();
      if (snapshot.runs.maze.revealed) $("maze-continue").focus({ preventScroll: true });
    }
  } catch (error) {
    actionError(error, "maze-answer-status");
  }
});
$("maze-continue").addEventListener("click", async () => {
  const m = snapshot?.runs.maze;
  if (!m?.pending || !m.revealed || pending) return;
  try {
    await rpc("maze_continue", { run_id: m.id, question_key: m.question.key });
  } catch (error) {
    actionError(error, "maze-answer-status");
  }
});
function renderMazeEnd(m) {
  const box = $("maze-end-content");
  box.replaceChildren();
  if (m.status === "lost")
    box.innerHTML =
      '<div class="dragon-stage" aria-hidden="true"><span class="kid">🧒</span><span class="dragon">🐉</span></div><h3>הַדְּרָקוֹן הַשּׁוֹבָב הִגִּיעַ!</h3><p>לֹא נוֹרָא! נְנַסֶּה שׁוּב וְנִשְׁתַּפֵּר.</p>';
  else
    box.innerHTML =
      '<div class="end-icon" aria-hidden="true">' +
      (m.status === "passed" ? "🏆" : "🌱") +
      "</div><h3>" +
      (m.status === "passed"
        ? "כָּל הַכָּבוֹד! הָרָמָה הֻשְׁלְמָה."
        : "הִגַּעְנוּ לַדֶּגֶל! נְנַסֶּה שׁוּב לְ־80%.") +
      "</h3>";
  const score = document.createElement("p");
  score.innerHTML = `הַצִּיּוּן ${n(fixed(m.score) + " / 100")} נִשְׁמַר בַּדֵּרוּג.`;
  box.append(score);
  if (m.status === "passed" && m.level < 2) {
    const next = document.createElement("button");
    next.className = "btn";
    next.textContent = "לָרָמָה הַבָּאָה ←";
    serverButton(next);
    next.addEventListener("click", () =>
      rpc("start", { activity: "maze", level: m.level + 1 }).catch(actionError),
    );
    box.append(next);
  }
  const again = document.createElement("button");
  again.className = "btn secondary";
  again.textContent = "נִסָּיוֹן חָדָשׁ · שְׁלוֹשָׁה לְבָבוֹת";
  serverButton(again);
  again.addEventListener("click", () => rpc("maze_restart", { run_id: m.id }).catch(actionError));
  box.append(again);
}
$("maze-restart").addEventListener("click", () => {
  const m = snapshot?.runs.maze;
  if (!m) return;
  if (!restartConfirm && m.status === "active") {
    restartConfirm = true;
    renderMaze();
    return;
  }
  restartConfirm = false;
  rpc("maze_restart", { run_id: m.id }).catch((error) => actionError(error, "maze-status"));
});

function renderRanking() {
  const s = snapshot;
  $("ranking-class").textContent = "הַדֵּרוּג הַמְּשֻׁתָּף שֶׁל כִּתָּה " + s.player.class_name;
  $("my-average").textContent = fixed(s.stats.average);
  $("my-games").textContent = s.stats.games;
  $("my-rank").textContent = s.leaderboard.find((x) => x.self)?.rank || "—";
  const body = $("ranking-body");
  body.replaceChildren();
  for (const row of s.leaderboard) {
    const tr = document.createElement("tr");
    if (row.self) tr.className = "self";
    const values = [
      row.rank,
      row.first_name + " " + row.last_name,
      row.class_name,
      fixed(row.average),
      row.games,
    ];
    values.forEach((value, i) => {
      const td = document.createElement("td");
      td.textContent = value;
      if ([0, 3, 4].includes(i)) td.className = "numeric-cell";
      if (i === 1) td.className = "name-cell";
      tr.append(td);
    });
    body.append(tr);
  }
  $("ranking-empty").hidden = !!s.leaderboard.length;
  const history = $("history-list");
  history.replaceChildren();
  for (const row of s.recent) {
    const el = document.createElement("div");
    el.className = "history-row";
    const text = document.createElement("div");
    text.textContent =
      GAME_NAMES[row.activity] +
      (row.activity === "table" ? "" : " · רָמָה " + LEVEL_NAMES[row.level]);
    const date = document.createElement("small");
    const bdi = document.createElement("bdi");
    bdi.textContent = new Date(row.finished * 1000).toLocaleString("he-IL", {
      dateStyle: "short",
      timeStyle: "short",
    });
    date.append(bdi);
    text.append(date);
    const score = document.createElement("bdi");
    score.className = "history-score";
    score.textContent = fixed(row.score);
    el.append(text, score);
    history.append(el);
  }
  if (!s.recent.length) {
    const empty = document.createElement("p");
    empty.className = "subtle";
    empty.textContent = "הַתּוֹצָאוֹת יוֹפִיעוּ כָּאן אַחֲרֵי סִיּוּם הַמִּשְׂחָק הָרִאשׁוֹן.";
    history.append(empty);
  }
  serverButton($("refresh-ranking"));
}
$("refresh-ranking").addEventListener("click", () => rpc("sync").catch(actionError));
setInterval(() => {
  if (page === "ranking" && snapshot && !pending && document.visibilityState === "visible")
    rpc("sync").catch(actionError);
}, 25000);
createTable();
message("streamlit:componentReady", { apiVersion: 1 });
if ("ResizeObserver" in window) new ResizeObserver(resizeFrame).observe($("app"));
window.addEventListener("resize", resizeFrame);
resizeFrame();

</script>
</body></html>'''

def run_streamlit():
    import tempfile
    import logging
    import streamlit as st
    import streamlit.components.v1 as components

    st.set_page_config(page_title='לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא',page_icon='🌱',layout='wide')
    st.markdown('''<style>
    .stApp,[data-testid="stAppViewContainer"]{background:#f7f5ee}
    [data-testid="stMainBlockContainer"],.block-container{max-width:1100px;padding:.5rem .25rem 1rem}
    [data-testid="stHeader"]{display:none}
    @media(max-width:600px){[data-testid="stMainBlockContainer"],.block-container{padding:.25rem 0 .5rem}}
    </style>''',unsafe_allow_html=True)

    def setting(key):
        if os.environ.get(key): return os.environ[key]
        try: return st.secrets.get(key)
        except (FileNotFoundError,KeyError): return None

    database_url=setting('SHAKED_DATABASE_URL')
    # Local development is opt-in. A cloud deployment never silently falls back
    # to an ephemeral SQLite file and pretends that pupils' data is durable.
    dev_path=os.environ.get('SHAKED_DEV_DB') if not database_url else None

    @st.cache_resource
    def service_for(url,local_path):
        db=Database(url=url,dev_path=local_path)
        db.initialize()
        return Classroom(db)

    service=None
    if database_url or dev_path:
        try: service=service_for(database_url,dev_path)
        except Exception as exc:
            logging.getLogger('shaked').warning('Database initialization failed: %s',type(exc).__name__)
            st.error('לא ניתן להתחבר לשמירה המשותפת כרגע. בעל האתר יכול לבדוק את הגדרת החיבור ולנסות שוב.')
    else:
        with st.expander('הגדרה חד־פעמית לבעל האתר — הפעלת המשחק הכיתתי',expanded=False):
            st.write('כדי להפעיל כניסת שחקנים ודירוג משותף, יש לחבר מסד PostgreSQL קבוע. '
                     'מוסיפים ב־Settings → Secrets של האפליקציה את SHAKED_DATABASE_URL עם מחרוזת החיבור. '
                     'הוראות מלאות נמצאות בחבילה המצורפת. אין להכניס סיסמאות לקוד או למאגר GitHub.')
    if dev_path: st.caption('מצב בדיקה מקומי — אינו השמירה המשותפת של האתר הציבורי.')

    @st.cache_resource
    def frontend_directory(html):
        directory=Path(tempfile.mkdtemp(prefix='shaked_classroom_'))
        (directory/'index.html').write_text(html,encoding='utf-8')
        return str(directory)

    widget=components.declare_component('shaked_multiplication',path=frontend_directory(APP_HTML))
    request=widget(configured=service is not None,snapshot=st.session_state.get('public_snapshot'),
                   response=st.session_state.get('classroom_response'),key='shaked_classroom_v4',default=None)
    if not isinstance(request,dict): return
    request_id=request.get('id')
    if request_id==st.session_state.get('handled_request_id'): return
    st.session_state.handled_request_id=request_id
    response={'id':request_id,'ok':False}
    try:
        if not service: raise UserError('הַכְּנִיסָה הַכִּתָּתִית עֲדַיִן אֵינָהּ זְמִינָה.')
        if not isinstance(request_id,str) or not re.fullmatch('[A-Za-z0-9_-]{8,100}',request_id):
            raise UserError('נִרְעֲנֵן אֶת הַדַּף וְנַמְשִׁיךְ.')
        action=request.get('action');payload=request.get('payload',{})
        if not isinstance(payload,dict): raise UserError('פְּעֻלָּה לֹא תַּקִּינָה.')
        if action in ('register','login'):
            pid=service.authenticate(action,payload)
            st.session_state.player_id=pid
            response.update(ok=True,snapshot=service.snapshot(pid))
        elif action=='logout':
            st.session_state.pop('player_id',None)
            response.update(ok=True,snapshot=None)
        else:
            pid=st.session_state.get('player_id')
            if not pid: raise UserError('קֹדֶם נִכָּנֵס עִם הַשֵּׁם וְהַקּוֹד.')
            response.update(service.perform(pid,action,payload,request_id),ok=True)
    except UserError as exc:
        response['error']=str(exc)
        # A stale question from a second device must refresh to the authoritative
        # state, while rejected actions must never change attempts or grades.
        pid=st.session_state.get('player_id')
        if pid and service:
            try: response['snapshot']=service.snapshot(pid)
            except Exception: pass
    except Exception as exc:
        logging.getLogger('shaked').warning('Classroom action failed: %s',type(exc).__name__)
        response['error']='לֹא הִצְלַחְנוּ לְעַדְכֵּן כָּעֵת. נְרַעֲנֵן אֶת הַמַּצָּב לִפְנֵי שֶׁנַּמְשִׁיךְ.'
    if 'snapshot' in response: st.session_state.public_snapshot=response['snapshot']
    st.session_state.classroom_response=response
    st.rerun()


if __name__=='__main__':
    run_streamlit()
