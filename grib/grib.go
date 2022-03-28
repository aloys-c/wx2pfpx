package main

//go build -buildmode=c-shared -o go_grib.so
//go run ""./grib/grib.go"

//message.Section4.ProductDefinitionTemplate.FirstSurface.Value is the pressure altitude in Pa

//fmt.Println(messages[0].Section4.ProductDefinitionTemplate.ParameterCategory) gives measure type :T 00, u 22 and v 23
//fmt.Println(messages[0].Section4.ProductDefinitionTemplate.ParameterNumber)

import (
	"encoding/json"
	"fmt"
	"griblib"
	"log"
	"math"
	"os"
	"strconv"
)

import "C"

//export parse_grib
func parse_grib(dic string, n int, interp int, res_i int) *C.char {
	//fmt.Println("Hello, World")
	res := float64(res_i) / 100
	print(res)
	var stations []station

	json.Unmarshal([]byte(dic), &stations)

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

		fmt.Println(int(float64(i) / 27.0 * 100))

		for _, station := range stations {

			lon := station.Lon
			lat := station.Lat

			if interp == 1 {
				lon_l, lon_h, lat_l, lat_h := get_l_h(lon, lat, res)
				dist := []float64{get_dist(lon, lat, lon_l, lat_h), get_dist(lon, lat, lon_h, lat_h), get_dist(lon, lat, lon_h, lat_l), get_dist(lon, lat, lon_l, lat_l)}
				i_p := []int{get_i(lat_h, lon_l, res), get_i(lat_h, lon_h, res), get_i(lat_l, lon_h, res), get_i(lat_l, lon_l, res)}

				u_p := []float64{u[i_p[0]], u[i_p[1]], u[i_p[2]], u[i_p[3]]}
				v_p := []float64{v[i_p[0]], v[i_p[1]], v[i_p[2]], v[i_p[3]]}
				T_p := []float64{temp[i_p[0]], temp[i_p[1]], temp[i_p[2]], temp[i_p[3]]}
				w_p := get_weigths(dist)

				sum_u := weighted_sum(u_p, w_p)
				sum_v := weighted_sum(v_p, w_p)
				sum_T := weighted_sum(T_p, w_p)

				x, y, speed, head := get_wind(sum_u, sum_v)
				stations[k].Data = append(station.Data, data{Pa2feet(float64(alt)), int(sum_T - 273.15), x, y, speed, head})
			} else {
				index := get_i(lat, lon, res)
				x, y, speed, head := get_wind(u[index], v[index])
				stations[k].Data = append(station.Data, data{Pa2feet(float64(alt)), int(temp[index] - 273.15), x, y, speed, head})
			}
			k += 1
		}
	}
	json, err := json.Marshal(stations)
	if err != nil {
		log.Fatalf("Error occured during marshaling. Error: %s", err.Error())
	}
	//fmt.Print(string(json[1:400]))
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

type station struct {
	Icao  string  `json:"code"`
	Lat   float64 `json:"lat"`
	Lon   float64 `json:"lon"`
	Alt   float64 `json:"alt"`
	Metar string  `json:"METAR"`
	Taf   string  `json:"TAF"`
	Data  []data  `json:"data"`
}

func weighted_sum(v []float64, w [4]float64) float64 {
	return v[0]*w[0] + v[1]*w[1] + v[2]*w[2] + v[3]*w[3]
}

func get_weigths(dist []float64) [4]float64 {
	var w [4]float64
	for i := 0; i < 4; i++ {
		w[i] = (1 / dist[i]) / (1/dist[0] + 1/dist[1] + 1/dist[2] + 1/dist[3])
	}
	return w
}

func get_dist(x1 float64, y1 float64, x2 float64, y2 float64) float64 {
	dx := math.Abs(x2 - x1)
	dy := math.Abs(y2 - y1)
	return math.Sqrt(dx*dx + dy*dy)
}

func get_l_h(x float64, y float64, res float64) (float64, float64, float64, float64) {
	x_l := math.Floor(x/res) * res
	x_h := math.Ceil(x/res) * res
	y_l := math.Floor(y/res) * res
	y_h := math.Ceil(y/res) * res
	return x_l, x_h, y_l, y_h
}

func round_p(x float64, res float64) float64 {
	return math.Round(x/res) * res
}

func Pa2feet(pa float64) int {
	return int((1 - math.Pow(pa/(100.0*1013.25), 0.190284)) * 145366.45)
}

func get_i(lat float64, lon float64, res float64) int {

	Ni := 360 / res
	//Nj := 180/res+1

	i := int((180-round_p(lat+90, res))/res*Ni + math.Mod(round_p(lon+360, res), 360)*(1/(res))) //Ni or Nj
	return i
}

func get_wind(u float64, v float64) (float64, float64, float64, int) {
	x := u
	y := v
	return x, y, math.Pow((math.Pow(x, 2)+math.Pow(y, 2)), 0.5) * 1.943, int((math.Atan2(x, y)*180/math.Pi)+360) % 360
}

func main() {
	print("/")
	print(get_i(-90, -0.25, 0.25))
	print("/")
	print(get_i(-90, -0.5, 0.5))
	print("/")
	print(get_i(-90, -1, 1))
}
