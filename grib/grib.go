package main

//go build -buildmode=c-shared -o go_grib.so
//go run ""./grib/grib.go"

//message.Section4.ProductDefinitionTemplate.FirstSurface.Value is the pressure altitude in Pa

//fmt.Println(messages[0].Section4.ProductDefinitionTemplate.ParameterCategory) gives measure type :T 00, u 22 and v 23
//fmt.Println(messages[0].Section4.ProductDefinitionTemplate.ParameterNumber)

import (
	"encoding/json"
	"griblib"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strconv"
)

import "C"

//export parse_grib
func parse_grib(n int, typ int) *C.char {
	//fmt.Println("Hello, World")

	var airports []airport
	var file string

	if typ == 2 {
		file = "./data/met_taf"
	} else if typ == 1 {
		file = "./data/grid"
	} else {
		file = "./data/stations"
	}

	arpts, err := ioutil.ReadFile(file)
	if err != nil {
		log.Fatalf("Could not open test-file %v", err)
	}

	json.Unmarshal([]byte(arpts), &airports)

	gribfile, err := os.Open("./data/data." + strconv.Itoa(n))
	messages, err := griblib.ReadMessages(gribfile)

	if err != nil {
		log.Fatalf("Could not open test-file %v", err)
	}

	for i := 0; i < 27; i += 3 {
		temp := messages[i].Data()
		u := messages[i+1].Data()
		v := messages[i+2].Data()
		k := 0
		alt := messages[i].Section4.ProductDefinitionTemplate.FirstSurface.Value
		for _, airport := range airports {

			lon := airport.Lon
			lat := airport.Lat

			index := get_i(lat, lon)

			x, y, speed, head := get_wind(u[index], v[index])
			airports[k].Data = append(airport.Data, data{Pa2feet(float64(alt)), int(temp[index] - 273.15), x, y, speed, head})
			k += 1
		}
	}
	json, err := json.Marshal(airports)
	if err != nil {
		log.Fatalf("Error occured during marshaling. Error: %s", err.Error())
	}
	//fmt.Print(string(json[1:4000]))
	return C.CString(string(json))
}

type data struct {
	Altitude int     `json:"altitude"`
	T        int     `json:"T"`
	U        float64 `json:"u"`
	V        float64 `json:"v"`
	Speed    float64 `json:"speed"`
	Head     int     `json:"head"`
}

type airport struct {
	Icao  string  `json:"code"`
	Lat   float64 `json:"lat"`
	Lon   float64 `json:"lon"`
	Alt   float64 `json:"alt"`
	Metar string  `json:"METAR"`
	Taf   string  `json:"TAF"`
	Data  []data  `json:"data"`
}

type station struct {
	Code string  `json:"ICAO"`
	Lat  float64 `json:"lat"`
	Lon  float64 `json:"lon"`
	Alt  float64 `json:"alt"`
	Data []data  `json:"data"`
}

var Nj = 181.0
var Ni = 360.0

func Pa2feet(pa float64) int {
	return int((1 - math.Pow(pa/(100.0*1013.25), 0.190284)) * 145366.45)
}

func get_i(lat float64, lon float64) int {
	i := int((180-math.Round(lat+90))*Ni + math.Mod(math.Round(lon+360), 360)) //Ni or Nj
	return i
}

func get_wind(u float64, v float64) (float64, float64, float64, int) {
	x := u
	y := v
	return x, y, math.Pow((math.Pow(x, 2)+math.Pow(y, 2)), 0.5) * 1.943, int((math.Atan2(x, y)*180/math.Pi)+360) % 360
}

func main() {
	parse_grib(0, 1)
}
