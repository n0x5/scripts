// Unfinished script to parse big xml file
// Learning Go so this is just a test
// https://discogs-data-dumps.s3.us-west-2.amazonaws.com/index.html?prefix=data/2023/

package main

import (
    "encoding/xml"
    "fmt"
    "os"
    "strings"
)

type Release struct {
    XMLName xml.Name `xml:"release"`
    Style     []string    `xml:"styles>style"`
    Genre     []string    `xml:"genres>genre"`
    Label     Label    `xml:"labels>label"`
    Track     []Track    `xml:"tracklist>track"`
    RelTitle    string   `xml:"title"`
    MasterID    int   `xml:"master_id"`
    ID    int   `xml:"id"`
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
            fmt.Printf("%s - %d - %d - %s - %s - %s - %v - %v - %d - %s - %s - %v\n", b.Released, b.MasterID, b.ID, b.RelTitle, b.Country, b.Artist, 
                        strings.Join(b.Genre, ", "), strings.Join(b.Style, ", "), b.Label.ID, b.Label.Name, b.Label.Catno, b.Track)
        }
    }
}


