#!/bin/bash

pytest tests -v --cov=cad_to_h5m --cov-append --cov-report term --cov-report xml
