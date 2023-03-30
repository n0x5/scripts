// Unfinished script to parse big xml file into sqlite3
// On windows need: https://jmeubank.github.io/tdm-gcc/
// Learning Go so this is just a test
// https://discogs-data-dumps.s3.us-west-2.amazonaws.com/index.html?prefix=data/2023/

package main

import (
    "encoding/xml"
    "fmt"
    "os"
    "strings"
    "database/sql"
    "log"
    _ "github.com/mattn/go-sqlite3"
)


type Release struct {
    XMLName xml.Name `xml:"release"`
    Style     []string    `xml:"styles>style"`
    Genre     []string    `xml:"genres>genre"`
    Label     Label    `xml:"labels>label"`
    Track     []Track    `xml:"tracklist>track"`
    RelTitle    string   `xml:"title"`
    MasterID    int   `xml:"master_id"`
    ID    int   `xml:"id,attr"`
    Country    string   `xml:"country"`
    Released    string   `xml:"released"`
    Artist      string   `xml:"artists>artist>name"`
}

type Label struct {
    Name    string  `xml:"name,attr"`
    Catno    string  `xml:"catno,attr"`
    ID    int  `xml:"id,attr"`
}

type Track struct {
    Position    string  `xml:"position"`
    Title    string  `xml:"title"`
    Duration    string  `xml:"duration"`
}

func main() {
    db, err := sql.Open("sqlite3", "test555.db")
    var i int
    if err != nil {
        log.Fatal(err)
    }

    sql1 := `create table if not exists discogs (released text, master_id int, id int, rel_title text, country text, 
            artist text, genres text, styles text, label_id int, label_name text, label_catno text, tracklist text);`
    _, err = db.Exec(sql1)

    if err != nil {
        log.Fatal(err)
    }

    xmlFile, err := os.Open("discogs_20230301_releases.xml")
    if err != nil {
        fmt.Println(err)
    }

    fmt.Println("Successfully Opened releases.xml")
    defer xmlFile.Close()
    d := xml.NewDecoder(xmlFile)
    for {
        t, tokenErr := d.Token()
        if tokenErr != nil {
            fmt.Println(err)
        }
        switch t := t.(type) {
        case xml.StartElement:
            b := &Release{}
            if err := d.DecodeElement(&b, &t); err != nil {
                fmt.Println(err)
            }
            sql2 := fmt.Sprintf(`insert into discogs (released, master_id, id, rel_title, country, artist, genres, styles, label_id, label_name, label_catno, tracklist) values ('%s','%d','%d','%s','%s','%s','%v','%v','%d','%s','%s','%v');\n`, b.Released, b.MasterID, b.ID, b.RelTitle, b.Country, b.Artist, 
                       strings.Join(b.Genre, ", "), strings.Join(b.Style, ", "), b.Label.ID, b.Label.Name, b.Label.Catno, b.Track)
            _, err = db.Exec(sql2)
            i++;
            fmt.Println(i)
        }
    }
    defer db.Close()
}

