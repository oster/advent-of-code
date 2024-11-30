```
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg


 '0':   a,b,c,_,e,f,g   6 segments   
 '1':   _,_,c,_,_,f,_   2 segments   (unique)
 '2':   a,_,c,d,e,_,g   5 segments
 '3':   a,_,c,d,_,f,g   5 segments
 '4':   _,b,c,d,_,f,_   4 segments   (unique)
 '5':   a,b,_,d,_,f,g   5 segments
 '6':   a,b,_,d,e,f,g   6 segments
 '7':   a,_,c,_,_,f,_   3 segments   (unique)
 '8':   a,b,c,d,e,f,g   7 segments   (unique)
 '9':   a,b,c,d,_,f,g   6 segments



disovering process:

 '1':   _,_,c,_,_,f,_   2 segments  (unique)

 '7':   a,_,c,_,_,f,_   3 segments  (unique)

 '4':   _,b,c,d,_,f,_   4 segments  (unique)

 '3':   a,_,c,d,_,f,g   5 segments  (includes 7, 1)

 '2':   a,_,c,d,e,_,g   5 segments  (does not include 7, 1)
 '5':   a,b,_,d,_,f,g   5 segments  (does not include 7, 1 but included in 6)

 '6':   a,b,_,d,e,f,g   6 segments  (does not include 7, 1)
 '0':   a,b,c,_,e,f,g   6 segments  (includes 7, 1)
 '9':   a,b,c,d,_,f,g   6 segments  (includes 7, 1 but includes 3, 4)

 '8':   a,b,c,d,e,f,g   7 segments  (unique)
```