package main

import (
	"encoding/csv"
	"flag"
	"io"
	"log"
	"net/http"
	"os"
	"path"
	"strconv"
)

var (
	host      string
	port      string
	dataSize  int
	baseIndex int
	outputDir string
)

func init() {
	flag.StringVar(&host, "host", "localhost", "host of the securimage server")
	flag.StringVar(&port, "port", ":8080", "port of the securimage server")
	flag.IntVar(&dataSize, "dataSize", 100, "number of data generated")
	flag.IntVar(&baseIndex, "baseIndex", 0, "base index of data")
	flag.StringVar(&outputDir, "outputDir", "./crawler/data", "output directory")
}

func generate(fileName string) string {
	resp, err := http.Get("http://" + host + port)
	if err != nil {
		log.Fatal("fail to get image from server", err.Error())
	}
	defer resp.Body.Close()

	filePath := path.Join(outputDir, fileName)

	f, err := os.Create(filePath)
	if err != nil {
		log.Fatal("fail to create output file")
	}
	defer f.Close()

	if _, err := io.Copy(f, resp.Body); err != nil {
		log.Fatal("fail to copy image to file")
	}

	code := resp.Header.Get("x-captcha-code")

	return code
}

func main() {
	flag.Parse()

	if err := os.MkdirAll(outputDir, 0755); err != nil {
		log.Fatal("fail to mkdir output dir")
	}

	var csvRows [][]string

	for i := 0; i < dataSize; i++ {
		fileName := "captcha-" + strconv.Itoa(baseIndex+i) + ".png"

		code := generate(fileName)

		csvRows = append(csvRows, []string{fileName, code})

		if i%100 == 0 {
			log.Printf("progress: %%%f\n", float64(i)/float64(dataSize)*100)
		}
	}

	csvFilePath := path.Join(outputDir, "label.csv")
	csvFile, err := os.Create(csvFilePath)
	if err != nil {
		log.Fatal("fail to create csv file")
	}
	defer csvFile.Close()

	if err := csv.NewWriter(csvFile).WriteAll(csvRows); err != nil {
		log.Fatal("fail to write csv file")
	}

	log.Println("done")
}
