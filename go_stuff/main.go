package main

import (
	"encoding/hex"
	"fmt"

	"golang.org/x/crypto/curve25519"
)

func main() {
	scalar, err := hex.DecodeString("4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d")
	if err != nil {
		panic(err)
	}
	point, err := hex.DecodeString("e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493")
	if err != nil {
		panic(err)
	}
	out, err := curve25519.X25519(scalar, point)
	if err != nil {
		panic(err)
	}
	fmt.Println(hex.EncodeToString(out))
}
