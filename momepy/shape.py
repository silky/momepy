#!/usr/bin/env python
# -*- coding: utf-8 -*-

# shape.py
# definitons of shape characters

import geopandas as gpd
from tqdm import tqdm  # progress bar
import math
import random
import numpy as np
from shapely.geometry import Point


def form_factor(objects, column_name, area_column, volume_column):
    """
    Calculate form factor of each object in given geoDataFrame.

    .. math::
        area \over {volume^{2 \over 3}}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    volume_column : str
        name of the column where is stored volume value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Bourdic, L., Salat, S. and Nowacki, C. (2012) ‘Assessing cities: a new system
    of cross-scale spatial indicators’, Building Research & Information, 40(5),
    pp. 592–605. doi: 10.1080/09613218.2012.703488self.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating form factor...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        if row[volume_column] is not 0:
            objects.loc[index, column_name] = row[area_column] / (row[volume_column] ** (2 / 3))

        else:
            objects.loc[index, column_name] = 0

    print('Form factor calculated.')
    return objects


def fractal_dimension(objects, column_name, area_column, perimeter_column):
    """
    Calculate fractal dimension of each object in given geoDataFrame.

    .. math::
        {log({{perimeter} \over {4}})} \over log(area)

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    perimeter_column : str
        name of the column where is stored perimeter value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Hermosilla, T. et al. (2014) ‘Using street based metrics to characterize urban
    typologies’, Computers, Environment and Urban Systems, 44, pp. 68–79.
    doi: 10.1016/j.compenvurbsys.2013.12.002.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating fractal dimension...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = math.log(row[perimeter_column] / 4) / math.log(row[area_column])

    print('Fractal dimension calculated.')
    return objects


def volume_facade_ratio(objects, column_name, volume_column, perimeter_column, height_column):
    """
    Calculate volume/facade ratio of each object in given geoDataFrame.

    .. math::
        volume \over perimeter * heigth

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    volume_column : str
        name of column where is stored volume value
    perimeter_column : str
        name of the column where is stored perimeter value
    height_column : str
        name of the column where is stored height value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ----------
    Schirmer, P. M. and Axhausen, K. W. (2015) ‘A multiscale classification of
    urban morphology’, Journal of Transport and Land Use, 9(1), pp. 101–130.
    doi: 10.5198/jtlu.2015.667.

    Notes
    -----
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating volume/facade ratio...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[volume_column] / (row[perimeter_column] * row[height_column])

    print('Volume/facade ratio calculated.')
    return objects


# Smallest enclosing circle - Library (Python)

# Copyright (c) 2017 Project Nayuki
# https://www.nayuki.io/page/smallest-enclosing-circle

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program (see COPYING.txt and COPYING.LESSER.txt).
# If not, see <http://www.gnu.org/licenses/>.

# Data conventions: A point is a pair of floats (x, y). A circle is a triple of floats (center x, center y, radius).

# Returns the smallest circle that encloses all the given points. Runs in expected O(n) time, randomized.
# Input: A sequence of pairs of floats or ints, e.g. [(0,5), (3.1,-2.7)].
# Output: A triple of floats representing a circle.
# Note: If 0 points are given, None is returned. If 1 point is given, a circle of radius 0 is returned.
#
# Initially: No boundary points known


def make_circle(points):
    # Convert to float and randomize order
    shuffled = [(float(x), float(y)) for (x, y) in points]
    random.shuffle(shuffled)

    # Progressively add points to circle or recompute circle
    c = None
    for (i, p) in enumerate(shuffled):
        if c is None or not is_in_circle(c, p):
            c = _make_circle_one_point(shuffled[: i + 1], p)
    return c


# One boundary point known
def _make_circle_one_point(points, p):
    c = (p[0], p[1], 0.0)
    for (i, q) in enumerate(points):
        if not is_in_circle(c, q):
            if c[2] == 0.0:
                c = make_diameter(p, q)
            else:
                c = _make_circle_two_points(points[: i + 1], p, q)
    return c


# Two boundary points known
def _make_circle_two_points(points, p, q):
    circ = make_diameter(p, q)
    left = None
    right = None
    px, py = p
    qx, qy = q

    # For each point not in the two-point circle
    for r in points:
        if is_in_circle(circ, r):
            continue

        # Form a circumcircle and classify it on left or right side
        cross = _cross_product(px, py, qx, qy, r[0], r[1])
        c = make_circumcircle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0 and (left is None or _cross_product(px, py, qx, qy, c[0], c[1]) > _cross_product(px, py, qx, qy, left[0], left[1])):
            left = c
        elif cross < 0.0 and (right is None or _cross_product(px, py, qx, qy, c[0], c[1]) < _cross_product(px, py, qx, qy, right[0], right[1])):
            right = c

    # Select which circle to return
    if left is None and right is None:
        return circ
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left[2] <= right[2]) else right


def make_circumcircle(p0, p1, p2):
    # Mathematical algorithm from Wikipedia: Circumscribed circle
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
    oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
    ax -= ox
    ay -= oy
    bx -= ox
    by -= oy
    cx -= ox
    cy -= oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = math.hypot(x - p0[0], y - p0[1])
    rb = math.hypot(x - p1[0], y - p1[1])
    rc = math.hypot(x - p2[0], y - p2[1])
    return (x, y, max(ra, rb, rc))


def make_diameter(p0, p1):
    cx = (p0[0] + p1[0]) / 2.0
    cy = (p0[1] + p1[1]) / 2.0
    r0 = math.hypot(cx - p0[0], cy - p0[1])
    r1 = math.hypot(cx - p1[0], cy - p1[1])
    return (cx, cy, max(r0, r1))


_MULTIPLICATIVE_EPSILON = 1 + 1e-14


def is_in_circle(c, p):
    return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] * _MULTIPLICATIVE_EPSILON


# Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2).
def _cross_product(x0, y0, x1, y1, x2, y2):
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
# end of Nayuiki script to define the smallest enclosing circle


def compactness_index(objects, column_name, area_column):
    """
    Calculate compactness index of each object in given geoDataFrame.

    .. math::
        area \over \\textit{area of enclosing circle}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative Science of Urban
    Form. University of Strathclyde.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating compactness index...')

    # calculate the area of circumcircle
    def circle_area(points):
        circ = make_circle(points)
        return(math.pi * circ[2] ** 2)

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        objects.loc[index, column_name] = (row[area_column]) / (circle_area(list(row['geometry'].convex_hull.exterior.coords)))

    print('Compactness index calculated.')
    return objects


def compactness_index2(objects, column_name, area_column, perimeter_column):
    """
    Calculate compactness index of each object in given geoDataFrame.

    .. math::
        {\\sqrt{area}} \over {perimeter}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    perimeter_column : str
        name of the column of objects gdf where is stored perimeter value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Feliciotti A (2018) RESILIENCE AND URBAN DESIGN:A SYSTEMS APPROACH TO THE
    STUDY OF RESILIENCE IN URBAN FORM. LEARNING FROM THE CASE OF GORBALS. Glasgow.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating compactness index...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        objects.loc[index, column_name] = (math.sqrt(row[area_column])) / (row[perimeter_column])

    print('Compactness index calculated.')
    return objects


def convexeity(objects, column_name, area_column):
    """
    Calculate convexeity index of each object in given geoDataFrame.

    .. math::
        area \over \\textit{convex hull area}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative Science of Urban
    Form. University of Strathclyde.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating convexeity...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[area_column] / (row['geometry'].convex_hull.area)

    print('Convexeity calculated.')
    return objects


def courtyard_index(objects, column_name, area_column, courtyard_column):
    """
    Calculate courtyard index of each object in given geoDataFrame.

    .. math::
        \\textit{area of courtyards} \over \\textit{total area}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    courtyard_column : str
        name of column where is stored courtyard area

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Schirmer, P. M. and Axhausen, K. W. (2015) ‘A multiscale classification of
    urban morphology’, Journal of Transport and Land Use, 9(1), pp. 101–130.
    doi: 10.5198/jtlu.2015.667.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating courtyard index...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[courtyard_column] / row[area_column]

    print('Courtyard index calculated.')
    return objects


def rectangularity(objects, column_name, area_column):
    """
    Calculate rectangularity of each object in given geoDataFrame.

    .. math::
        {area \over \\textit{minimum bounding rotated rectangle area}}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative Science of Urban
    Form. University of Strathclyde.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating rectangularity...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = row[area_column] / (row['geometry'].minimum_rotated_rectangle.area)

    print('Rectangularity calculated.')
    return objects


def shape_index(objects, column_name, area_column, longest_axis_column):
    """
    Calculate shape index of each object in given geoDataFrame.

    .. math::
        {\\sqrt{{area} \over {\\pi}}} \over {0.5 * \\textit{longest axis}}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    longest_axis_column : str
        name of column where is stored longest axis value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Ale?

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating shape index...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            objects.loc[index, column_name] = math.sqrt(row[area_column] / math.pi) / (0.5 * row[longest_axis_column])

    print('Shape index calculated.')
    return objects


def corners(objects, column_name):
    """
    Calculate number of corners of each object in given geoDataFrame.

    Uses only external shape (shapely.geometry.exterior), courtyards are not included.

    .. math::
        count

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------

    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating corners...')

    # calculate angle between points, return true or false if real corner
    def true_angle(a, b, c):
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        if np.degrees(angle) <= 170:
            return True
        elif np.degrees(angle) >= 190:
            return True
        else:
            return False

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        corners = 0  # define empty variables
        points = list(row['geometry'].exterior.coords)  # get points of a shape
        stop = len(points) - 1  # define where to stop
        for i in np.arange(len(points)):  # for every point, calculate angle and add 1 if True angle
            if i == 0:
                    continue
            elif i == stop:
                a = np.asarray(points[i - 1])
                b = np.asarray(points[i])
                c = np.asarray(points[1])

                if true_angle(a, b, c) is True:
                    corners = corners + 1
                else:
                    continue

            else:
                a = np.asarray(points[i - 1])
                b = np.asarray(points[i])
                c = np.asarray(points[i + 1])

                if true_angle(a, b, c) is True:
                    corners = corners + 1
                else:
                    continue

        objects.loc[index, column_name] = corners

    print('Corners calculated.')
    return objects


def squareness(objects, column_name):
    """
    Calculate squareness of each object in given geoDataFrame.

    Uses only external shape (shapely.geometry.exterior), courtyards are not included.

    .. math::
        \\textit{mean deviation of all corners from 90 degrees}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ----------
    Dibble, J. (2016) Urban Morphometrics: Towards a Quantitative Science of Urban
    Form. University of Strathclyde.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating squareness...')

    def angle(a, b, c):
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(cosine_angle))

        return angle

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        angles = []
        points = list(row['geometry'].exterior.coords)  # get points of a shape
        stop = len(points) - 1  # define where to stop
        for i in np.arange(len(points)):  # for every point, calculate angle and add 1 if True angle
            if i == 0:
                    continue
            elif i == stop:
                a = np.asarray(points[i - 1])
                b = np.asarray(points[i])
                c = np.asarray(points[1])
                ang = angle(a, b, c)

                if ang <= 175:
                    angles.append(ang)
                elif angle(a, b, c) >= 185:
                    angles.append(ang)
                else:
                    continue

            else:
                a = np.asarray(points[i - 1])
                b = np.asarray(points[i])
                c = np.asarray(points[i + 1])
                ang = angle(a, b, c)

                if angle(a, b, c) <= 175:
                    angles.append(ang)
                elif angle(a, b, c) >= 185:
                    angles.append(ang)
                else:
                    continue
        deviations = []
        for i in angles:
            dev = abs(90 - i)
            deviations.append(dev)
        objects.loc[index, column_name] = np.mean(deviations)

    print('Squareness calculated.')
    return objects


def equivalent_rectangular_index(objects, column_name, area_column, perimeter_column):
    """
    Calculate equivalent rectangular index of each object in given geoDataFrame.

    .. math::
        \\sqrt{{area} \over \\textit{area of bounding rectangle}} * {\\textit{perimeter of bounding rectangle} \over {perimeter}}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    perimeter_column : str
        name of the column of objects gdf where is stored perimeter value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Basaraner M and Cetinkaya S (2017) Performance of shape indices and classification
    schemes for characterising perceptual shape complexity of building footprints in GIS.
    2nd ed. International Journal of Geographical Information Science, Taylor & Francis
    31(10): 1952–1977. Available from:
    https://www.tandfonline.com/doi/full/10.1080/13658816.2017.1346257.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating equivalent rectangular index...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            bbox = row['geometry'].minimum_rotated_rectangle
            objects.loc[index, column_name] = math.sqrt(row[area_column] / bbox.area) * (bbox.length / row[perimeter_column])

    print('Equivalent rectangular index calculated.')
    return objects


def elongation(objects, column_name):
    """
    Calculate elongation of object seen as elongation of its minimum bounding rectangle.

    .. math::
        {{p - \\sqrt{p^2 - 16a}} \over {4}} \over {{{p} \over {2}} - {{p - \\sqrt{p^2 - 16a}} \over {4}}}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Gil J, Montenegro N, Beirão JN, et al. (2012) On the Discovery of
    Urban Typologies: Data Mining the Multi-dimensional Character of
    Neighbourhoods. Urban Morphology 16(1): 27–40.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating elongation...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            bbox = row['geometry'].minimum_rotated_rectangle
            a = bbox.area
            p = bbox.length
            cond1 = (p ** 2)
            cond2 = (16 * a)
            if cond1 >= cond2:
                sqrt = cond1 - cond2
            else:
                sqrt = 0

            # calculate both width/length and length/width
            elo1 = ((p - math.sqrt(sqrt)) / 4) / ((p / 2) - ((p - math.sqrt(sqrt)) / 4))
            elo2 = ((p + math.sqrt(sqrt)) / 4) / ((p / 2) - ((p + math.sqrt(sqrt)) / 4))
            # use the smaller one (e.g. shorter/longer)
            if elo1 <= elo2:
                elo = elo1
            else:
                elo = elo2

            objects.loc[index, column_name] = elo

    print('Elongation calculated.')
    return objects


def centroid_corners(objects, column_name):
    """
    Calculate mean distance centroid - corners.

    .. math::
        \\textit{mean distance centroid - corners}

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ----------
    Schirmer PM and Axhausen KW (2015) A multiscale classiﬁcation of urban morphology.
    Journal of Transport and Land Use 9(1): 101–130.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating mean distance centroid - corner...')

    # calculate angle between points, return true or false if real corner
    def true_angle(a, b, c):
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        if np.degrees(angle) <= 170:
            return True
        elif np.degrees(angle) >= 190:
            return True
        else:
            return False

    # iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
        distances = []  # set empty list of distances
        centroid = row['geometry'].centroid  # define centroid
        points = list(row['geometry'].exterior.coords)  # get points of a shape
        stop = len(points) - 1  # define where to stop
        for i in np.arange(len(points)):  # for every point, calculate angle and add 1 if True angle
            if i == 0:
                    continue
            elif i == stop:
                a = np.asarray(points[i - 1])
                b = np.asarray(points[i])
                c = np.asarray(points[1])
                p = Point(points[i])

                if true_angle(a, b, c) is True:
                    distance = centroid.distance(p)  # calculate distance point - centroid
                    distances.append(distance)  # add distance to the list
                else:
                    continue

            else:
                a = np.asarray(points[i - 1])
                b = np.asarray(points[i])
                c = np.asarray(points[i + 1])
                p = Point(points[i])

                if true_angle(a, b, c) is True:
                    distance = centroid.distance(p)
                    distances.append(distance)
                else:
                    continue

        objects.loc[index, column_name] = np.mean(distances)  # calculate mean and sve it to DF
    print('Mean distances centroid - corner calculated.')
    return objects


def linearity(objects, column_name, length_column):
    """
    Calculate linearity of each LineString object in given geoDataFrame.

    .. math::
        Ratio between Euclidean distance and segment length.

    Parameters
    ----------
    objects : GeoDataFrame
        GeoDataFrame containing objects
    column_name : str
        name of the column to save the values
    area_column : str
        name of the column of objects gdf where is stored area value
    perimeter_column : str
        name of the column of objects gdf where is stored perimeter value

    Returns
    -------
    GeoDataFrame
        GeoDataFrame with new column [column_name] containing resulting values.

    References
    ---------
    Basaraner M and Cetinkaya S (2017) Performance of shape indices and classification
    schemes for characterising perceptual shape complexity of building footprints in GIS.
    2nd ed. International Journal of Geographical Information Science, Taylor & Francis
    31(10): 1952–1977. Available from:
    https://www.tandfonline.com/doi/full/10.1080/13658816.2017.1346257.

    Notes
    -------
    Option to calculate without area and volume being calculated beforehand.
    """
    # define new column
    objects[column_name] = None
    objects[column_name] = objects[column_name].astype('float')
    print('Calculating equivalent rectangular index...')

    # fill new column with the value of area, iterating over rows one by one
    for index, row in tqdm(objects.iterrows(), total=objects.shape[0]):
            bbox = row['geometry'].minimum_rotated_rectangle
            objects.loc[index, column_name] = math.sqrt(row[area_column] / bbox.area) * (bbox.length / row[perimeter_column])

    print('Equivalent rectangular index calculated.')
    return objects
# to be deleted, keep at the end

# path = "/Users/martin/Strathcloud/Personal Folders/Test data/Royston/buildings.shp"
# objects = gpd.read_file(path)
# # #
# # # convexeity(objects, 'conv', 'pdbAre')
# # #
# # # objects.head
# # # objects.to_file(path)
# corners(objects, 'corners')
