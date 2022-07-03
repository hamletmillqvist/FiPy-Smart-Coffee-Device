# My Smart Coffee Machine
<img width="100%" src="https://i.imgur.com/wte7EUL.png" alt="example of notification from discord" style="margin-bottom:10px;" />

###### tags: `IoT` `WLAN` `MQTT` `FiPy` `Pysense 2.0 X` `MicroPython` `MCP9700` `Webhooks`

**Date of publish:** 2022-07-03
**Author:** [Magnusson Millqvist, Hamlet](https://www.linkedin.com/in/hamletmillqvist/) (hm222vx)
**Inquiries:** :mailbox: [hamlet.millqvist@pm.me](mailto:hamlet.millqvist@pm.me)

## Introduction
This tutorial presents a solution for notifying the user when they have forgotten to retrieve freshly heated coffee/tea (or any other heated beverage really) before it goes cold again. By only utilising a temperature sensor, programmable microcontroller, connection to the web, and an online database with ability to push webhooks!

This project was done as part of the course Applied internet of things at Linnaeus University, Sweden. All provided imagery, text, and code posted here is available free of use under a slightly modified MIT license provided further down. You are basically free to do whatever you want with any information found in this tutorial as long as you include a copy of the copyright and a mention of where you got it from! Just a thank you to 'Magnusson Millqvist' for providing the code for (this or that) is just fine by me.

**Used parts:**
* FiPy with headers
* Pysense 2.0 X
* Micro USB cable
* Breadboard
* Shielded copper wires
* MCP9700 (Temperature sensor)

:::info
:timer_clock: This project range between an hour to a few hours to set up.
:::

# Table of Contents
[toc]

# Project Description
This project tackles the simple problems of an average computer programmer, like forgetting your newly heated coffee! :coffee: 

You see, dear reader, I have a tendency of forgetting that I've made coffee, continuing my work while letting the one beverage I enjoy the most- cool down to lukewarm temperature. When entering the course in *Applied internet of things* and being asked to provide a solution to something, it dawned on me that this was the perfect opportunity to attempt solving my problem!

## The Plan
After some thinking and planing in my head I decided that I could easily build a solution with only the temperature sensor `MPC9700`, which is one of the many provided sensor at the [**electrokit bundle**](https://www.electrokit.com/en/product/lnu-1dt305-tillampad-iot-fipy-and-sensors-bundle/) available for the course. My plan was simple, by measuring the temperature at short intervals, I could easily determine the state my coffee machine is currently in. By determining my its states as either `Cold`, `Heating up`, `Hot`, or `Cooling down` and using simple logic triggering events on state changes, combined with the internal CPU clock, I could determine if my coffee has been standing hot for a prolonged period of time.

# Copyright Notice
Copyright (c) 2022 Hamlet Magnusson Millqvist

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Any material used must be presented together with a reference to either the publication source *(https://hackmd.io/@hm222vx/SmartCoffeeMachine)* , code source *()*, or the author *(Magnusson Millqvist, Hamlet)*.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
