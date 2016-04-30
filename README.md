# Lucifer's Screwdriver

![Lucifer's Screwdriver Logo](/doc/img/lucifiers-screwdriver-logo.png)

Lucifer's Screwdriver is a project created for the NASA Space Apps 2016
challenge: "Near Earth Objects Machine Learning". It was the winner of the "Galactic Problem-Solver" award, at the event hosted by the Rochester Institute of Technology.

This is a proof-of-concept for using machine learning to identify Potentially Hazardous Asteroids (PHA). The standard definition of a PHA is an asteroid whose closest approach to Earth is below a threshold, and whose brightness is over a threshold. We use an existing tool to compute the distance of closest approach from orbital parameters reported by the Minor Planet Center, and then train a supervised classifier to identify the PHAs.

[Youtube Video](https://www.youtube.com/watch?v=cBQzAnGjzi4)

[NASA Space Apps 2016](https://2016.spaceappschallenge.org/challenges/solar-system/near-earth-objects-machine-learning/projects/lucifers-screwdriver)

# Installing

To run the code, download the source code from this repository using your method of choice. It was developed using Python 3.5, so while other versions may still work, they remain untested. Enter the directory containing the source code, and run

```bash
$ python setup.py install
```

You may need to do this as a root user, depending on your system settings.

This should pull in the required dependencies (`numpy>=1.10.0` and `scikit-learn>0.17.1`).

You can then run the program with

```bash
$ lucifers-screwdriver --help
```


# Data

Data in the [MPCORB format](http://www.minorplanetcenter.net/iau/info/MPOrbitFormat.html) are taken from the Minor Planet Center's website ([download link for latest complete data set (large file)](http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT)).


# Minimum Orbit Intersection Distance (MOID) Simulations

We use existing software written by Giovanni Federico Gronchi, which takes orbital parameters, and computes critical points in the orbits. It takes the orbital parameters:

1. perihelion distance (AU)
2. eccentricity
3. inclination (J2000 degrees)
4. longitude of ascending node (J2000 degrees)
5. argument of periapsis (J2000 degrees)

We take the global minimum distance from this output as the MOID.

To run this code, you must compile G. Gronchi's code yourself. The code is available [here](http://adams.dm.unipi.it/~gronchi/HOMEPAGE/research.html). It uses the proprietary Intel compiler by default, so if you would like to use a free alternative (e.g. `gfortran`), edit the file `make.flags`, and change `FC=ifort` to a free compiler (e.g. `FC=gfortran`), and remove the `FFLAGS` line. Then compile it with `make all`. You will need to provide the executable `CP_comp.x` to Lucifer's Screwdriver, so take note of its location.

To compute the MOIDs, and save them to a file, run Lucifer's Screwdriver with

```bash
$ lucifers-screwdriver --orbit-data <MPCORB file> \
      sim --MOID-exe <CP_comp.x> --MOID-output <MOID file>
```

where `<MPCORB file>` is downloaded from the Minor Planet Center website, `<CP_comp.x>` is the path to the executable mentioned earlier, and `<MOID file>` is the file you'd like to save the calculated MOIDs to.

(Note: we make use of "Allen's Astrophysical Quantities", 4th Edition, by Arthur N. Cox for the orbital parameters of Earth. ISBN 978-1-4612-1186-0)


# Machine Learning with k-Nearest Neighbor

Once we have found the MOIDs for each asteroid, we check if it is less than 0.05 [AU](https://en.wikipedia.org/wiki/Astronomical_unit), and if its absolute brightness as reported by the MPC satisfies `H < 22.0`. If it meets these two criteria, it is flagged as a Potentially Hazardous Asteroid.

We then train a [kNN classifier](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) on the orbital parameters, and H, with whether it is a PHA as the label. You can do this by running

```bash
$ lucifers-screwdriver --orbit-data <MPCORB file> \
      learn --MOID-input <MOID file> --n-neighbors <k>
```

where `<MPCORB file>` and `<MOID file>` are the same files mentioned earlier, and `<k>` is an integer (1 or greater) representing the number of neighbors to use in the classification. If you set `k = 1`, you are cheating, and will just get the original labels. Setting `k` higher will consider other objects. In practice, you should do the training on one set of objects, and the predictions on another set. Read about [cross validation](https://en.wikipedia.org/wiki/Cross-validation_%28statistics%29) for more on this.


# Performance and Improvements

Ultimately we find our method to be less effective than we would like. Using `k = 2` correctly identifies 3.99% of PHA's, and has no false positives. Raising `k` gives progressively worse results.

Still, the basic structure of the method is effective. With the use of a better classifier than kNN, as well as additional features for training, this has the potential to be effective. [Deep Learning](https://en.wikipedia.org/wiki/Deep_learning) is a popular classification method today, due to its powerful capabilities, and if time had permitted, we would have used it instead of kNN.


# Name

You have likely wondered why this is called "Lucifer's Screwdriver". It is a play on the title of the 1977 book "Lucifer's Hammer", written by Larry Niven and Jerry Pournelle. The book is about a comet impact destroying civilization on Earth. Our title is an homage to the book, and we elected to use the word "screwdriver" because it is a more precise tool for fixing problems ... okay not really, it just sounded funny.


# Credit

Coding: [Daniel Wysocki](http://dwysocki.github.io/)

Video: Juan Lachapelle, [Justin Flory](https://github.com/jflory7), and [Daniel Wysocki](http://dwysocki.github.io/)

Logo: [Guan-Huei Wu](https://www.behance.net/mystory5)
