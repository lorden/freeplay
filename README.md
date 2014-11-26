FreePlay
==========

![FreePlay GUI](https://raw.githubusercontent.com/lorden/freeplay/master/freeplay.png)

This is an experiment to connect my Ubuntu machine to one or many
Apple TVs. It includes scanning the network, sending a picture or fake-mirroring.
Mirroring is achieved by taking a screenshot with scrot and sending these pictures
to the devices at 1fps.

## Requirements
- [Scrot](http://linuxbrit.co.uk/scrot/)
- [PyQt4](https://wiki.python.org/moin/PyQt)

## Notes
This software is quite unstable but it works.
To run the program:
```
python freeplayer.py
```

Major credit to [Clément Vasseur](https://github.com/nto) and [his guide](http://nto.github.io/AirPlay.html)

After a while of tinkering with the protocol it became pretty clear that Apple doesn't want to open this device.
But if you feel like improving this piece of software, feel free to do so, a lot can be improved here.
