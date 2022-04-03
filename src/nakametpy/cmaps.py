# Copyright 2021 nakamura_yuki
# 
# This program comes from Qiita article
# URL: https://qiita.com/vpcf/items/b680f504cfe8b6a64222
#  
# 他のカラーマップに関してはMatplotlibやgeocat-vizで対応可能
#
# To Do
# - get_colormapで存在しないカラーマップを指定した際に、
# 　(自作の？)エラーを表示させるようにする
#
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import sys


_CMAX = 255

def sunshine():
    r'''
    NCLのcolor table中の `sunshine_9lev` に対応する。
    levelは256である。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----    
    オブジェクトは ``sunshine_256lev`` という名前でも受け取れる。

    |sunshine|

    .. |sunshine| image:: ./img/sunshine.png
       :width: 600
    '''
    cdict = {'red':   [(0.0,  1.0, 1.0),
                    (0.8,  1.0, 1.0),
                    (1.0,  0.7, 0.7)],
            'green': [(0.0,  1.0, 1.0),
                    (0.6,  0.7, 0.7),
                    (1.0,  0.2, 0.2)],
            'blue':  [(0.0,  1.0, 1.0),
                    (0.3,  0.2, 0.2),
                    (0.6,  0.2, 0.2),
                    (0.8,  0.0, 0.0),
                    (0.9,  0.2, 0.2),
                    (1.0,  0.1, 0.1)]}         
    return LinearSegmentedColormap('sunshine', cdict)


def BrWhGr():
    r'''
    緑白ブラウンのカラーマップ。
    水蒸気の発散収束を表す際に便利。
    levelは256である。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----    
    オブジェクトは ``BrWhGr_256lev`` という名前でも受け取れる。

    |BrWhGr|

    .. |BrWhGr| image:: ./img/BrWhGr.png
        :width: 600
    '''
    cdict = {'red':   [(0.0,  0.4, 0.4),
                    (0.4,  1.0, 1.0),
                    (0.5,  1.0, 1.0),
                    (0.9,  0.0, 0.0),
                    (1.0,  0.0, 0.0)],

            'green': [(0.0,  0.3, 0.3),
                    (0.2,  0.45, 0.45),
                    (0.5, 1.0, 1.0),
                    (0.8, 1.0, 1.0),
                    (1.0, 0.5, 0.5)],

            'blue':  [(0.0,  0.2, 0.2),
                    (0.2,  0.3, 0.3),
                    (0.5,  1.0, 1.0),
                    (0.9,  0.0, 0.0),
                    (1.0,  0.0, 0.0)]}
    return LinearSegmentedColormap('BrWhGr', cdict)


def precip3():
    r'''降水量をプロットする際に利用することを想定したカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``precip3_256lev`` という名前でも受け取れる。

    |precip3|

    .. |precip3| image:: ./img/precip3.png
        :width: 600
    '''
    cdict = {'red':   [(0.0,  1.0, 1.0),
                    (0.2,  0.4, 0.4),
                    (0.375,  0.0, 0.0),
                    (0.5,  0., 0.0),
                    (0.55, 0.4, 0.4),
                    (0.75,  1.0, 1.0),
                    (1.0,  1.0, 1.0)],

            'green': [(0.0,  1., 1.),
                    (0.15, .7, .7),
                    (0.375,  .4, .4),
                    (0.55, 1.0, 1.0),
                    (0.75, 1.0, 1.0),
                    (0.95, .5, .5),
                    (1.0, 0.1, 0.1)],

            'blue':  [(0.0,  1., 1.),
                    (0.2, 1., 1.),
                    (0.275, 0.95, 0.95),
                    (0.35, 1., 1.),
                    (0.5,  0.2, 0.2),
                    (0.55, 0.0, 0.0),
                    (0.65, 0.2, 0.2),
                    (0.75, 0., 0.),
                    (1.0,  0.0, 0.0)]}
    return LinearSegmentedColormap('precip3', cdict)



    
def jma_linear():
    r'''気象庁が降水量をプロットする際に利用しているカラーマップを模している。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``jma_linear_256lev`` という名前でも受け取れる。

    |jma_linear|

    .. |jma_linear| image:: ./img/jma_linear.png
        :width: 600

    See Also
    --------
    jma_list
    '''
    cdict = {'red':   [(0.0,  180/_CMAX, 180/_CMAX),
                  (1/7, 1., 1.),
                  (2/7, 1., 1.),
                   (3/7,  250/_CMAX, 0.),
                  (4/7, 33/_CMAX, 33/_CMAX),
                   (5/7,  160/_CMAX, 160/_CMAX),
                   (6/7,  242/_CMAX, 242/_CMAX),
                   (1, 1, 1)],

         'green': [(0.0,  0, 0),
                   (1/7, 40/_CMAX, 40/_CMAX),
                  (2/7, 153/_CMAX, 153/_CMAX),
                   (3/7, 245/_CMAX, 65/_CMAX),
                   (4/7, 140/_CMAX, 140/_CMAX),
                   (5/7, 210/_CMAX, 210/_CMAX),
                   (6/7, 242/_CMAX, 242/_CMAX),
                   (1,1,1)],

         'blue':  [(0.0,  104/_CMAX, 104/_CMAX),
                   (1/7, 0, 0),
                  (2/7, 0, 0),
                   (3/7,  0., 1.),
                   (4/7, 1., 1.),
                   (5/7, 1., 1.),
                   (6/7,  1., 1.),
                   (1,1,1)]}
    return LinearSegmentedColormap('jma_linear', cdict).reversed()


def jma_list():
    r'''気象庁が降水量をプロットする際に利用しているカラーマップを模している。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``jma_list_9lev`` という名前でも受け取れる。

    |jma_list|

    .. |jma_list| image:: ./img/jma_list.png
        :width: 600

    See Also
    --------
    jma_linear
    '''
    clist = [[180/_CMAX, 0, 104/_CMAX],
            [1., 40/_CMAX, 0],
            [1., 153/_CMAX, 0],
            [250/_CMAX, 245/_CMAX, 0],
            [0, 65/_CMAX, 1],
            [33/_CMAX, 140/_CMAX, 1],
            [160/_CMAX, 210/_CMAX, 1],
            [242/_CMAX, 242/_CMAX, 1],
            [1, 1, 1]]
            # [242/_CMAX, 242/_CMAX, 1]]
    return ListedColormap(clist, 'jma_list').reversed()


def grads_default_rainbow_linear():
    r'''GrADSデフォルトのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_default_rainbow_linear_256lev`` という名前でも受け取れる。

    |grads_default_rainbow_linear|

    .. |grads_default_rainbow_linear| image:: ./img/grads_default_rainbow_linear.png
        :width: 600

    See Also
    --------
    grads_default_rainbow_list
    '''
    cdict = {'red':   [(0.0,  160/_CMAX, 160/_CMAX),
                    (1/12, 130/_CMAX, 130/_CMAX),
                    (2/12, 30/_CMAX, 30/_CMAX),
                    (3/12, 0/_CMAX, 0/_CMAX),
                    (4/12, 0/_CMAX, 0/_CMAX),
                    (5/12, 0/_CMAX, 0/_CMAX),
                    (6/12, 0/_CMAX, 0/_CMAX),
                    (7/12, 160/_CMAX, 160/_CMAX),
                    (8/12, 230/_CMAX, 230/_CMAX),
                    (9/12, 230/_CMAX, 230/_CMAX),
                    (10/12, 240/_CMAX, 240/_CMAX),
                    (11/12, 250/_CMAX, 250/_CMAX),
                    (12/12, 240/_CMAX, 240/_CMAX)],

            'green': [(0.0,  0, 0),
                    (1/12, 0, 0),
                    (2/12, 60/_CMAX, 60/_CMAX),
                    (3/12, 160/_CMAX, 160/_CMAX),
                    (4/12, 200/_CMAX, 200/_CMAX),
                    (5/12, 210/_CMAX, 210/_CMAX),
                    (6/12, 220/_CMAX, 220/_CMAX),
                    (7/12, 230/_CMAX, 230/_CMAX),
                    (8/12, 220/_CMAX, 220/_CMAX),
                    (9/12, 175/_CMAX, 175/_CMAX),
                    (10/12, 130/_CMAX, 130/_CMAX),
                    (11/12, 60/_CMAX, 60/_CMAX),
                    (12/12, 0/_CMAX, 0/_CMAX)],

            'blue':  [(0.0,  200/_CMAX, 200/_CMAX),
                    (1/12, 220/_CMAX, 220/_CMAX),
                    (2/12, 255/_CMAX, 255/_CMAX),
                    (3/12, 255/_CMAX, 255/_CMAX),
                    (4/12, 200/_CMAX, 200/_CMAX),
                    (5/12, 210/_CMAX, 210/_CMAX),
                    (6/12, 0/_CMAX, 0/_CMAX),
                    (7/12, 50/_CMAX, 50/_CMAX),
                    (8/12, 50/_CMAX, 50/_CMAX),
                    (9/12, 45/_CMAX, 45/_CMAX),
                    (10/12, 40/_CMAX, 40/_CMAX),
                    (11/12, 60/_CMAX, 60/_CMAX),
                    (12/12, 130/_CMAX, 130/_CMAX)]}
    return LinearSegmentedColormap('grads_default_rainbow_linear', cdict)


def grads_default_rainbow_list():
    r'''GrADSデフォルトのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_default_rainbow_list_13lev`` という名前でも受け取れる。

    |grads_default_rainbow_list|

    .. |grads_default_rainbow_list| image:: ./img/grads_default_rainbow_list.png
        :width: 600

    See Also
    --------
    grads_default_rainbow_linear
    '''
    clist = [[160/_CMAX, 0, 200/_CMAX],
        [130/_CMAX, 0, 220/_CMAX],
        [30/_CMAX, 60/_CMAX, 1],
        [0, 160/_CMAX, 1],
        [0, 200/_CMAX, 200/_CMAX],
        [0, 210/_CMAX, 210/_CMAX],
        [0, 220/_CMAX, 0],
        [160/_CMAX, 230/_CMAX, 50/_CMAX],
        [230/_CMAX, 225/_CMAX, 50/_CMAX],
        [230/_CMAX, 170/_CMAX, 45/_CMAX],
        [240/_CMAX, 130/_CMAX, 40/_CMAX],
        [250/_CMAX, 60/_CMAX, 60/_CMAX],
        [240/_CMAX, 0, 130/_CMAX]]
    return ListedColormap(clist, 'grads_default_rainbow_list')


def grads_paired():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_paired_256lev`` という名前でも受け取れる。

    |grads_paired|

    .. |grads_paired| image:: ./img/grads_paired.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.8824, 0.8824),
          (0.09, 0.698, 0.698),
          (0.18, 0.5333, 0.5333),
          (0.27, 0.1843, 0.1843),
          (0.36, 0.5922, 0.5922),
          (0.45, 0.1569, 0.1569),
          (0.55, 0.4, 0.4),
          (0.64, 0.0039, 0.0039),
          (0.73, 0.8235, 0.8235),
          (0.82, 0.6, 0.6),
          (0.91, 0.5882, 0.5882),
          (1.0, 0.1647, 0.1647)],

    'green': [(0.0, 0.8, 0.8),
            (0.09, 0.4824, 0.4824),
            (0.18, 0.8667, 0.8667),
            (0.27, 0.6353, 0.6353),
            (0.36, 0.5961, 0.5961),
            (0.45, 0.1529, 0.1529),
            (0.55, 0.7294, 0.7294),
            (0.64, 0.498, 0.498),
            (0.73, 0.6667, 0.6667),
            (0.82, 0.251, 0.251),
            (0.91, 0.9804, 0.9804),
            (1.0, 0.3647, 0.3647)],

    'red': [(0.0, 0.6353, 0.6353),
            (0.09, 0.1412, 0.1412),
            (0.18, 0.6824, 0.6824),
            (0.27, 0.2118, 0.2118),
            (0.36, 0.9804, 0.9804),
            (0.45, 0.898, 0.898),
            (0.55, 0.9922, 0.9922),
            (0.64, 0.9961, 0.9961),
            (0.73, 0.7647, 0.7647),
            (0.82, 0.4235, 0.4235),
            (0.91, 0.9922, 0.9922),
            (1.0, 0.702, 0.702)]}
    return LinearSegmentedColormap('grads_paired', cdict)

def grads_spectral():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_spectral_256lev`` という名前でも受け取れる。

    |grads_spectral|

    .. |grads_spectral| image:: ./img/grads_spectral.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
          (0.12, 0.5569, 0.5569),
          (0.25, 0.7765, 0.7765),
          (0.38, 0.8667, 0.8667),
          (0.5, 0.0471, 0.0471),
          (0.62, 0.0, 0.0),
          (0.75, 0.0, 0.0),
          (0.88, 0.0, 0.0),
          (1.0, 0.7647, 0.7647)],

    'green': [(0.0, 0.0, 0.0),
            (0.12, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.38, 0.549, 0.549),
            (0.5, 0.6039, 0.6039),
            (0.62, 1.0, 1.0),
            (0.75, 0.8353, 0.8353),
            (0.88, 0.0, 0.0),
            (1.0, 0.7647, 0.7647)],
            
    'red': [(0.0, 0.0, 0.0),
            (0.12, 0.4941, 0.4941),
            (0.25, 0.0, 0.0),
            (0.38, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.62, 0.051, 0.051),
            (0.75, 0.9804, 0.9804),
            (0.88, 0.8235, 0.8235),
            (1.0, 0.7647, 0.7647)]}
    return LinearSegmentedColormap('grads_spectral', cdict)

def grads_rainbow():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_rainbow_256lev`` という名前でも受け取れる。

    |grads_rainbow|

    .. |grads_rainbow| image:: ./img/grads_rainbow.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
          (0.17, 0.0, 0.0),
          (0.33, 0.0, 0.0),
          (0.5, 1.0, 1.0),
          (0.67, 1.0, 1.0),
          (0.83, 1.0, 1.0),
          (1.0, 0.0, 0.0)],

    'green': [(0.0, 0.0, 0.0),
            (0.17, 1.0, 1.0),
            (0.33, 1.0, 1.0),
            (0.5, 1.0, 1.0),
            (0.67, 0.0, 0.0),
            (0.83, 0.0, 0.0),
            (1.0, 0.0, 0.0)],

    'red': [(0.0, 1.0, 1.0),
            (0.17, 1.0, 1.0),
            (0.33, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.67, 0.0, 0.0),
            (0.83, 1.0, 1.0),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_rainbow', cdict)

def grads_b2r():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_b2r_256lev`` という名前でも受け取れる。

    |grads_b2r|

    .. |grads_b2r| image:: ./img/grads_b2r.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.3922, 0.3922),
          (0.25, 1.0, 1.0),
          (0.5, 1.0, 1.0),
          (0.75, 0.0, 0.0),
          (1.0, 0.0, 0.0)],

    'green': [(0.0, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.5, 1.0, 1.0),
            (0.75, 0.0, 0.0),
            (1.0, 0.0, 0.0)],
    
    'red': [(0.0, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.5, 1.0, 1.0),
            (0.75, 1.0, 1.0),
            (1.0, 0.3922, 0.3922)]}
    return LinearSegmentedColormap('grads_b2r', cdict)

def grads_brn2grn():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_brn2grn_256lev`` という名前でも受け取れる。

    |grads_brn2grn|

    .. |grads_brn2grn| image:: ./img/grads_brn2grn.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0196, 0.0196),
          (0.25, 0.5098, 0.5098),
          (0.5, 1.0, 1.0),
          (0.75, 0.7529, 0.7529),
          (1.0, 0.1961, 0.1961)],

    'green': [(0.0, 0.1922, 0.1922),
            (0.25, 0.7686, 0.7686),
            (0.5, 1.0, 1.0),
            (0.75, 0.7961, 0.7961),
            (1.0, 0.2431, 0.2431)],
            
    'red': [(0.0, 0.3333, 0.3333),
            (0.25, 0.8784, 0.8784),
            (0.5, 1.0, 1.0),
            (0.75, 0.4941, 0.4941),
            (1.0, 0.0, 0.0)]}
    return LinearSegmentedColormap('grads_brn2grn', cdict)

def grads_y2b():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_y2b_256lev`` という名前でも受け取れる。

    |grads_y2b|

    .. |grads_y2b| image:: ./img/grads_y2b.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0078, 0.0078),
          (0.25, 0.5137, 0.5137),
          (0.5, 1.0, 1.0),
          (0.75, 0.9922, 0.9922),
          (1.0, 0.9804, 0.9804)],

    'green': [(0.0, 0.8157, 0.8157),
            (0.25, 0.9098, 0.9098),
            (0.5, 1.0, 1.0),
            (0.75, 0.6392, 0.6392),
            (1.0, 0.1961, 0.1961)],
            
    'red': [(0.0, 0.9765, 0.9765),
            (0.25, 0.9882, 0.9882),
            (0.5, 1.0, 1.0),
            (0.75, 0.5686, 0.5686),
            (1.0, 0.0392, 0.0392)]}
    return LinearSegmentedColormap('grads_y2b', cdict)

def grads_oj2p():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_oj2p_256lev`` という名前でも受け取れる。

    |grads_oj2p|

    .. |grads_oj2p| image:: ./img/grads_oj2p.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0275, 0.0275),
          (0.25, 0.2039, 0.2039),
          (0.5, 1.0, 1.0),
          (0.75, 0.7176, 0.7176),
          (1.0, 0.2941, 0.2941)],

    'green': [(0.0, 0.2353, 0.2353),
            (0.25, 0.5961, 0.5961),
            (0.5, 1.0, 1.0),
            (0.75, 0.5137, 0.5137),
            (1.0, 0.0, 0.0)],
            
    'red': [(0.0, 0.5098, 0.5098),
            (0.25, 0.9216, 0.9216),
            (0.5, 1.0, 1.0),
            (0.75, 0.5569, 0.5569),
            (1.0, 0.1765, 0.1765)]}
    return LinearSegmentedColormap('grads_oj2p', cdict)

def grads_terrain1():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_terrain1_256lev`` という名前でも受け取れる。

    |grads_terrain1|

    .. |grads_terrain1| image:: ./img/grads_terrain1.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.6196, 0.6196),
          (0.2, 0.9961, 0.9961),
          (0.4, 0.4039, 0.4039),
          (0.6, 0.5922, 0.5922),
          (0.8, 0.3451, 0.3451),
          (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.2196, 0.2196),
            (0.2, 0.5961, 0.5961),
            (0.4, 0.8039, 0.8039),
            (0.6, 0.9922, 0.9922),
            (0.8, 0.3647, 0.3647),
            (1.0, 1.0, 1.0)],

    'red': [(0.0, 0.1882, 0.1882),
            (0.2, 0.0, 0.0),
            (0.4, 0.0196, 0.0196),
            (0.6, 0.9765, 0.9765),
            (0.8, 0.5059, 0.5059),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_terrain1', cdict)

def grads_ocean():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_ocean_256lev`` という名前でも受け取れる。

    |grads_ocean|

    .. |grads_ocean| image:: ./img/grads_ocean.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
          (0.33, 0.3098, 0.3098),
          (0.67, 0.7216, 0.7216),
          (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.4902, 0.4902),
            (0.33, 0.0314, 0.0314),
            (0.67, 0.5804, 0.5804),
            (1.0, 1.0, 1.0)],
            
    'red': [(0.0, 0.0, 0.0),
            (0.33, 0.0, 0.0),
            (0.67, 0.1608, 0.1608),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_ocean', cdict)

def grads_grayscale():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_grayscale_256lev`` という名前でも受け取れる。

    |grads_grayscale|

    .. |grads_grayscale| image:: ./img/grads_grayscale.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],
    'green': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],
    'red': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_grayscale', cdict)

def grads_red():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_red_256lev`` という名前でも受け取れる。

    |grads_red|

    .. |grads_red| image:: ./img/grads_red.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'green': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'red': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_red', cdict)

def grads_green():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_green_256lev`` という名前でも受け取れる。

    |grads_green|

    .. |grads_green| image:: ./img/grads_green.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'green': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],
    'red': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)]}
    return LinearSegmentedColormap('grads_green', cdict)

def grads_blue():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_blue_256lev`` という名前でも受け取れる。

    |grads_blue|

    .. |grads_blue| image:: ./img/grads_blue.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],
    'green': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'red': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)]}
    return LinearSegmentedColormap('grads_blue', cdict)

def grads_jet():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_jet_256lev`` という名前でも受け取れる。

    |grads_jet|

    .. |grads_jet| image:: ./img/grads_jet.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.5216, 0.5216),
          (0.12, 1.0, 1.0),
          (0.25, 1.0, 1.0),
          (0.38, 1.0, 1.0),
          (0.5, 0.8431, 0.8431),
          (0.62, 0.5176, 0.5176),
          (0.75, 0.0, 0.0),
          (0.88, 0.0, 0.0),
          (1.0, 0.0, 0.0)],

    'green': [(0.0, 0.0, 0.0),
            (0.12, 0.0, 0.0),
            (0.25, 0.3686, 0.3686),
            (0.38, 0.8196, 0.8196),
            (0.5, 1.0, 1.0),
            (0.62, 1.0, 1.0),
            (0.75, 1.0, 1.0),
            (0.88, 0.0, 0.0),
            (1.0, 0.0, 0.0)],
            
    'red': [(0.0, 0.0, 0.0),
            (0.12, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.38, 0.0, 0.0),
            (0.5, 0.1216, 0.1216),
            (0.62, 0.4471, 0.4471),
            (0.75, 1.0, 1.0),
            (0.88, 1.0, 1.0),
            (1.0, 0.5882, 0.5882)]}
    return LinearSegmentedColormap('grads_jet', cdict)

def grads_terrain2():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_terrain2_256lev`` という名前でも受け取れる。

    |grads_terrain2|

    .. |grads_terrain2| image:: ./img/grads_terrain2.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
            (0.17, 0.0235, 0.0235),
            (0.33, 0.1647, 0.1647),
            (0.5, 0.4471, 0.4471),
            (0.67, 0.6078, 0.6078),
            (0.83, 0.8667, 0.8667),
            (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.3412, 0.3412),
            (0.17, 0.5961, 0.5961),
            (0.33, 0.7176, 0.7176),
            (0.5, 0.6627, 0.6627),
            (0.67, 0.5922, 0.5922),
            (0.83, 0.8667, 0.8667),
            (1.0, 1.0, 1.0)],
    'red': [(0.0, 0.0, 0.0),

            (0.17, 0.2235, 0.2235),
            (0.33, 0.7059, 0.7059),
            (0.5, 0.6824, 0.6824),
            (0.67, 0.4941, 0.4941),
            (0.83, 0.8667, 0.8667),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_terrain2', cdict)

def grads_dark():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_dark_256lev`` という名前でも受け取れる。

    |grads_dark|

    .. |grads_dark| image:: ./img/grads_dark.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.4588, 0.4588),
            (0.14, 0.0196, 0.0196),
            (0.29, 0.698, 0.698),
            (0.43, 0.5373, 0.5373),
            (0.57, 0.1137, 0.1137),
            (0.71, 0.0078, 0.0078),
            (0.86, 0.1098, 0.1098),
            (1.0, 0.4039, 0.4039)],

    'green': [(0.0, 0.6157, 0.6157),
            (0.14, 0.3725, 0.3725),
            (0.29, 0.4353, 0.4353),
            (0.43, 0.1608, 0.1608),
            (0.57, 0.651, 0.651),
            (0.71, 0.6667, 0.6667),
            (0.86, 0.4627, 0.4627),
            (1.0, 0.4039, 0.4039)],

    'red': [(0.0, 0.1176, 0.1176),
            (0.14, 0.8392, 0.8392),
            (0.29, 0.4627, 0.4627),
            (0.43, 0.902, 0.902),
            (0.57, 0.4196, 0.4196),
            (0.71, 0.8824, 0.8824),
            (0.86, 0.651, 0.651),
            (1.0, 0.4039, 0.4039)]}
    return LinearSegmentedColormap('grads_dark', cdict)

def grads_snow():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_snow_256lev`` という名前でも受け取れる。

    |grads_snow|

    .. |grads_snow| image:: ./img/grads_snow.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.3529, 0.3529),
            (0.25, 0.7608, 0.7608),
            (0.5, 1.0, 1.0),
            (0.75, 1.0, 1.0),
            (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.3529, 0.3529),
            (0.25, 0.5725, 0.5725),
            (0.5, 1.0, 1.0),
            (0.75, 0.0, 0.0),
            (1.0, 0.0, 0.0)],

    'red': [(0.0, 0.3529, 0.3529),
            (0.25, 0.2824, 0.2824),
            (0.5, 0.0, 0.0),
            (0.75, 0.3922, 0.3922),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_snow', cdict)

def grads_satellite():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_satellite_256lev`` という名前でも受け取れる。

    |grads_satellite|

    .. |grads_satellite| image:: ./img/grads_satellite.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.75, 1.0, 1.0),
            (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.5, 1.0, 1.0),
            (0.75, 0.0, 0.0),
            (1.0, 1.0, 1.0)],

    'red': [(0.0, 0.0, 0.0),
            (0.25, 1.0, 1.0),
            (0.5, 1.0, 1.0),
            (0.75, 0.0, 0.0),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_satellite', cdict)

def grads_rain():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_rain_256lev`` という名前でも受け取れる。

    |grads_rain|

    .. |grads_rain| image:: ./img/grads_rain.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.75, 1.0, 1.0),
            (1.0, 1.0, 1.0)],

    'green': [(0.0, 1.0, 1.0),
            (0.25, 1.0, 1.0),
            (0.5, 0.0, 0.0),
            (0.75, 0.0, 0.0),
            (1.0, 0.6588, 0.6588)],

    'red': [(0.0, 0.0, 0.0),
            (0.25, 1.0, 1.0),
            (0.5, 1.0, 1.0),
            (0.75, 0.4706, 0.4706),
            (1.0, 0.0, 0.0)]}
    return LinearSegmentedColormap('grads_rain', cdict)

def grads_autumn():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_autumn_256lev`` という名前でも受け取れる。

    |grads_autumn|

    .. |grads_autumn| image:: ./img/grads_autumn.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 0.0, 0.0),
            (0.25, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.75, 0.5176, 0.5176),
            (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.0, 0.0),
            (0.25, 0.1059, 0.1059),
            (0.5, 0.498, 0.498),
            (0.75, 1.0, 1.0),
            (1.0, 1.0, 1.0)],

    'red': [(0.0, 0.0, 0.0),
            (0.25, 0.6078, 0.6078),
            (0.5, 1.0, 1.0),
            (0.75, 1.0, 1.0),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_autumn', cdict)

def grads_cool():
    r'''GrADSのcolormaps.gsのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_cool_256lev`` という名前でも受け取れる。

    |grads_cool|

    .. |grads_cool| image:: ./img/grads_cool.png
        :width: 600
    '''
    cdict = {'blue': [(0.0, 1.0, 1.0), 
            (0.33, 1.0, 1.0), 
            (0.67, 1.0, 1.0), 
            (1.0, 1.0, 1.0)],

    'green': [(0.0, 1.0, 1.0),
            (0.33, 0.6706, 0.6706),
            (0.67, 0.2627, 0.2627),
            (1.0, 0.0, 0.0)],

    'red': [(0.0, 0.0, 0.0),
            (0.33, 0.3294, 0.3294),
            (0.67, 0.7373, 0.7373),
            (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_cool', cdict)


def BlWhRe():
    r'''blue -> white -> red のカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``BlWhRe_256lev`` という名前でも受け取れる。

    |BlWhRe|

    .. |BlWhRe| image:: ./img/BlWhRe.png
        :width: 600
    '''
    _ncolor = 2
    cdict = {'blue':  [(0/_ncolor, 0/_CMAX, 0/_CMAX),
                   (1/_ncolor, 255/_CMAX, 255/_CMAX),
                   (2/_ncolor, 255/_CMAX, 255/_CMAX)],
    'green': [(0/_ncolor, 0/_CMAX, 0/_CMAX),
                   (1/_ncolor, 255/_CMAX, 255/_CMAX),
                   (2/_ncolor, 0/_CMAX, 0/_CMAX)],
    'red':   [(0/_ncolor,  255/_CMAX, 255/_CMAX),
                  (1/_ncolor, 255/_CMAX, 255/_CMAX),
                  (2/_ncolor, 0/_CMAX, 0/_CMAX)]}
    return LinearSegmentedColormap('grads_red', cdict).reversed()

def jma_temp_anom_linear():
    r'''dark blue -> blue -> light blue -> white -> yellow -> orange -> red

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_temp_anom_linear_256lev``.

    |jma_temp_anom_linear|

    .. |jma_temp_anom_linear| image:: ./img/jma_temp_anom_linear.png
        :width: 600
    '''
    _ncolor = 10
    cdict = {'blue':  [(0.0,  83/_CMAX, 83/_CMAX),
                  (1/_ncolor, 26/_CMAX, 26/_CMAX),
                  (2/_ncolor, 0/_CMAX, 0/_CMAX),
                  (3/_ncolor, 0/_CMAX, 0/_CMAX),
                  (4/_ncolor, 180/_CMAX, 180/_CMAX),
                  (5/_ncolor, 240/_CMAX, 240/_CMAX),
                  (6/_ncolor, 255/_CMAX, 255/_CMAX),
                  (7/_ncolor, 255/_CMAX, 255/_CMAX),
                  (8/_ncolor, 255/_CMAX, 255/_CMAX),
                  (9/_ncolor, 255/_CMAX, 255/_CMAX),
                 (10/_ncolor, 112/_CMAX, 112/_CMAX)],

              'green': [(0.0,  0, 0),
                   (1/_ncolor, 26/_CMAX, 26/_CMAX),
                   (2/_ncolor, 153/_CMAX, 153/_CMAX),
                   (3/_ncolor, 240/_CMAX, 240/_CMAX),
                   (4/_ncolor, 240/_CMAX, 240/_CMAX),
                   (5/_ncolor, 255/_CMAX, 255/_CMAX),
                   (6/_ncolor, 255/_CMAX, 255/_CMAX),
                   (7/_ncolor, 255/_CMAX, 255/_CMAX),
                   (8/_ncolor, 126/_CMAX, 126/_CMAX),
                   (9/_ncolor, 33/_CMAX, 33/_CMAX),
                   (10/_ncolor, 0/_CMAX, 0/_CMAX)],

              'red':   [(0.0,  145/_CMAX, 145/_CMAX),
                  (1/_ncolor, 255/_CMAX, 255/_CMAX),
                  (2/_ncolor, 255/_CMAX, 255/_CMAX),
                  (3/_ncolor, 255/_CMAX, 255/_CMAX),
                  (4/_ncolor, 255/_CMAX, 255/_CMAX),
                  (5/_ncolor, 255/_CMAX, 255/_CMAX),
                  (6/_ncolor, 200/_CMAX, 200/_CMAX),
                  (7/_ncolor, 70/_CMAX, 70/_CMAX),
                  (8/_ncolor, 0/_CMAX, 0/_CMAX),
                  (9/_ncolor, 33/_CMAX, 33/_CMAX),
                  (10/_ncolor, 0/_CMAX, 0/_CMAX)]}
    return LinearSegmentedColormap('jma_temp_anom_linear', cdict).reversed()


def jma_temp_anom_list():
    r'''dark blue -> blue -> light blue -> white -> yellow -> orange -> red

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_temp_anom_list_11lev``.

    |jma_temp_anom_list|

    .. |jma_temp_anom_list| image:: ./img/jma_temp_anom_list.png
        :width: 600

    See Also
    --------
    jma_temp_anom_linear
    '''
    clist = [[0.0, 0.0, 0.4392156862745098],
            [0.12941176470588237, 0.12941176470588237, 1.0],
            [0.0, 0.49411764705882355, 1.0],
            [0.27450980392156865, 1.0, 1.0],
            [0.7843137254901961, 1.0, 1.0],
            [1.0, 1.0, 0.9411764705882353],
            [1.0, 0.9411764705882353, 0.7058823529411765],
            [1.0, 0.9411764705882353, 0.0],
            [1.0, 0.6, 0.0],
            [1.0, 0.10196078431372549, 0.10196078431372549],
            [0.5686274509803921, 0, 0.3254901960784314]]
    return ListedColormap(clist, 'jma_temp_anom_list')

def jma_precip_anom_linear():
    r'''brown -> orange -> white -> limegreen -> green -> darkgreen

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_precip_anom_linear_256lev``.

    |jma_precip_anom_linear|

    .. |jma_precip_anom_linear| image:: ./img/jma_precip_anom_linear.png
        :width: 600
    '''
    _ncolor = 10
    cdict = {'blue':  [(0/_ncolor, 38/_CMAX, 38/_CMAX),
                   (1/_ncolor, 64/_CMAX, 64/_CMAX),
                   (2/_ncolor, 128/_CMAX, 128/_CMAX),
                   (3/_ncolor, 175/_CMAX, 175/_CMAX),
                   (4/_ncolor, 214/_CMAX, 214/_CMAX),
                   (5/_ncolor, 240/_CMAX, 240/_CMAX),
                   (6/_ncolor, 191/_CMAX, 191/_CMAX),
                   (7/_ncolor, 70/_CMAX, 70/_CMAX),
                   (8/_ncolor, 15/_CMAX, 15/_CMAX),
                   (9/_ncolor, 5/_CMAX, 5/_CMAX),
                   (10/_ncolor, 5/_CMAX, 5/_CMAX)],

              'green': [(0/_ncolor, 38/_CMAX, 38/_CMAX),
                   (1/_ncolor, 77/_CMAX, 77/_CMAX),
                   (2/_ncolor, 153/_CMAX, 153/_CMAX),
                   (3/_ncolor, 204/_CMAX, 204/_CMAX),
                   (4/_ncolor, 243/_CMAX, 243/_CMAX),
                   (5/_ncolor, 255/_CMAX, 255/_CMAX),
                   (6/_ncolor, 229/_CMAX, 229/_CMAX),
                   (7/_ncolor, 200/_CMAX, 200/_CMAX),
                   (8/_ncolor, 120/_CMAX, 120/_CMAX),
                   (9/_ncolor, 55/_CMAX, 55/_CMAX),
                   (10/_ncolor, 30/_CMAX, 30/_CMAX)],

              'red':   [(0/_ncolor,  0/_CMAX, 0/_CMAX),
                  (1/_ncolor, 0/_CMAX, 0/_CMAX),
                  (2/_ncolor, 0/_CMAX, 0/_CMAX),
                  (3/_ncolor, 31/_CMAX, 31/_CMAX),
                  (4/_ncolor, 73/_CMAX, 73/_CMAX),
                  (5/_ncolor, 255/_CMAX, 255/_CMAX),
                  (6/_ncolor, 255/_CMAX, 255/_CMAX),
                  (7/_ncolor, 255/_CMAX, 255/_CMAX),
                  (8/_ncolor, 245/_CMAX, 245/_CMAX),
                  (9/_ncolor, 120/_CMAX, 120/_CMAX),
                  (10/_ncolor, 60/_CMAX, 60/_CMAX)]}
    return LinearSegmentedColormap('jma_precip_anom_linear', cdict).reversed()

def jma_precip_anom_list():
    r'''brown -> orange -> white -> limegreen -> green -> darkgreen

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_precip_anom_list_11lev``.

    |jma_precip_anom_list|

    .. |jma_precip_anom_list| image:: ./img/jma_precip_anom_list.png
        :width: 600

    See Also
    --------
    jma_precip_anom_linear
    '''
    clist = [[0.23529411764705882, 0.11764705882352941, 0.0196078431372549],
            [0.47058823529411764, 0.21568627450980393, 0.0196078431372549],
            [0.9607843137254902, 0.47058823529411764, 0.058823529411764705],
            [1.0, 0.7843137254901961, 0.27450980392156865],
            [1.0, 0.8980392156862745, 0.7490196078431373],
            [1.0, 1.0, 0.9411764705882353],
            [0.28627450980392155, 0.9529411764705882, 0.8392156862745098],
            [0.12156862745098039, 0.8, 0.6862745098039216],
            [0.0, 0.6, 0.5019607843137255],
            [0.0, 0.30196078431372547, 0.25098039215686274],
            [0.0, 0.14901960784313725, 0.14901960784313725]]
    return ListedColormap(clist, 'jma_precip_anom_list')

def jma_sunlight_anom_linear():
    r'''indigo -> light purple -> white -> yellow -> orange -> red

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_sunlight_anom_linear_256lev``.

    |jma_sunlight_anom_linear|

    .. |jma_sunlight_anom_linear| image:: ./img/jma_sunlight_anom_linear.png
        :width: 600
    '''
    _ncolor = 10
    cdict = {'blue':  [(0/_ncolor, 83/_CMAX, 83/_CMAX),
                   (1/_ncolor, 26/_CMAX, 26/_CMAX),
                   (2/_ncolor, 0/_CMAX, 0/_CMAX),
                   (3/_ncolor, 0/_CMAX, 0/_CMAX),
                   (4/_ncolor, 180/_CMAX, 180/_CMAX),
                   (5/_ncolor, 240/_CMAX, 240/_CMAX),
                   (6/_ncolor, 255/_CMAX, 255/_CMAX),
                   (7/_ncolor, 243/_CMAX, 243/_CMAX),
                   (8/_ncolor, 119/_CMAX, 119/_CMAX),
                   (9/_ncolor, 80/_CMAX, 80/_CMAX),
                   (10/_ncolor, 56/_CMAX, 56/_CMAX)],

              'green': [(0/_ncolor, 0/_CMAX, 0/_CMAX),
                   (1/_ncolor, 26/_CMAX, 26/_CMAX),
                   (2/_ncolor, 153/_CMAX, 153/_CMAX),
                   (3/_ncolor, 240/_CMAX, 240/_CMAX),
                   (4/_ncolor, 240/_CMAX, 240/_CMAX),
                   (5/_ncolor, 255/_CMAX, 255/_CMAX),
                   (6/_ncolor, 238/_CMAX, 238/_CMAX),
                   (7/_ncolor, 210/_CMAX, 210/_CMAX),
                   (8/_ncolor, 74/_CMAX, 74/_CMAX),
                   (9/_ncolor, 36/_CMAX, 36/_CMAX),
                   (10/_ncolor, 0/_CMAX, 0/_CMAX)],

              'red':   [(0/_ncolor,  145/_CMAX, 145/_CMAX),
                  (1/_ncolor, 255/_CMAX, 255/_CMAX),
                  (2/_ncolor, 255/_CMAX, 255/_CMAX),
                  (3/_ncolor, 255/_CMAX, 255/_CMAX),
                  (4/_ncolor, 255/_CMAX, 255/_CMAX),
                  (5/_ncolor, 255/_CMAX, 255/_CMAX),
                  (6/_ncolor, 238/_CMAX, 238/_CMAX),
                  (7/_ncolor, 206/_CMAX, 206/_CMAX),
                  (8/_ncolor, 69/_CMAX, 69/_CMAX),
                  (9/_ncolor, 36/_CMAX, 36/_CMAX),
                  (10/_ncolor, 0/_CMAX, 0/_CMAX)]}
    return LinearSegmentedColormap('jma_sunlight_anom_linear', cdict).reversed()

def jma_sunlight_anom_list():
    r'''indigo -> light purple -> white -> yellow -> orange -> red

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_sunlight_anom_list_11lev``.

    |jma_sunlight_anom_list|

    .. |jma_sunlight_anom_list| image:: ./img/jma_sunlight_anom_list.png
        :width: 600

    See Also
    --------
    jma_sunlight_anom_linear
    '''
    clist = [[0.0, 0.0, 0.2196078431372549],
            [0.1411764705882353, 0.1411764705882353, 0.3137254901960784],
            [0.27058823529411763, 0.2901960784313726, 0.4666666666666667],
            [0.807843137254902, 0.8235294117647058, 0.9529411764705882],
            [0.9333333333333333, 0.9333333333333333, 1.0],
            [1.0, 1.0, 0.9411764705882353],
            [1.0, 0.9411764705882353, 0.7058823529411765],
            [1.0, 0.9411764705882353, 0.0],
            [1.0, 0.6, 0.0],
            [1.0, 0.10196078431372549, 0.10196078431372549],
            [0.5686274509803921, 0.0, 0.3254901960784314]]
    return ListedColormap(clist, 'jma_sunlight_anom_list')

def jma_snow_anom_linear():
    r'''brown -> orange -> white -> light blue -> blue -> slate blue

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_snow_anom_linear_256lev``.

    |jma_snow_anom_linear|

    .. |jma_snow_anom_linear| image:: ./img/jma_snow_anom_linear.png
        :width: 600
    '''
    _ncolor = 10
    cdict = {'blue':  [(0/_ncolor, 112/_CMAX, 112/_CMAX),
                   (1/_ncolor, 255/_CMAX, 255/_CMAX),
                   (2/_ncolor, 255/_CMAX, 255/_CMAX),
                   (3/_ncolor, 255/_CMAX, 255/_CMAX),
                   (4/_ncolor, 255/_CMAX, 255/_CMAX),
                   (5/_ncolor, 240/_CMAX, 240/_CMAX),
                   (6/_ncolor, 220/_CMAX, 220/_CMAX),
                   (7/_ncolor, 70/_CMAX, 70/_CMAX),
                   (8/_ncolor, 15/_CMAX, 15/_CMAX),
                   (9/_ncolor, 5/_CMAX, 5/_CMAX),
                   (10/_ncolor, 5/_CMAX, 5/_CMAX)],

              'green': [(0/_ncolor, 0/_CMAX, 0/_CMAX),
                   (1/_ncolor, 33/_CMAX, 33/_CMAX),
                   (2/_ncolor, 126/_CMAX, 126/_CMAX),
                   (3/_ncolor, 191/_CMAX, 191/_CMAX),
                   (4/_ncolor, 238/_CMAX, 238/_CMAX),
                   (5/_ncolor, 255/_CMAX, 255/_CMAX),
                   (6/_ncolor, 230/_CMAX, 230/_CMAX),
                   (7/_ncolor, 200/_CMAX, 200/_CMAX),
                   (8/_ncolor, 120/_CMAX, 120/_CMAX),
                   (9/_ncolor, 55/_CMAX, 55/_CMAX),
                   (10/_ncolor, 30/_CMAX, 30/_CMAX)],

              'red':   [(0/_ncolor,  0/_CMAX, 0/_CMAX),
                  (1/_ncolor, 33/_CMAX, 33/_CMAX),
                  (2/_ncolor, 0/_CMAX, 0/_CMAX),
                  (3/_ncolor, 0/_CMAX, 0/_CMAX),
                  (4/_ncolor, 153/_CMAX, 153/_CMAX),
                  (5/_ncolor, 255/_CMAX, 255/_CMAX),
                  (6/_ncolor, 255/_CMAX, 255/_CMAX),
                  (7/_ncolor, 255/_CMAX, 255/_CMAX),
                  (8/_ncolor, 245/_CMAX, 245/_CMAX),
                  (9/_ncolor, 120/_CMAX, 120/_CMAX),
                  (10/_ncolor, 60/_CMAX, 60/_CMAX)]}
    return LinearSegmentedColormap('jma_snow_anom_linear', cdict).reversed()

def jma_snow_anom_list():
    r'''brown -> orange -> white -> light blue -> blue -> slate blue

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_snow_anom_list_11lev``.

    |jma_snow_anom_list|

    .. |jma_snow_anom_list| image:: ./img/jma_snow_anom_list.png
        :width: 600

    See Also
    --------
    jma_snow_anom_linear
    '''
    clist = [[0.23529411764705882, 0.11764705882352941, 0.0196078431372549],
            [0.47058823529411764, 0.21568627450980393, 0.0196078431372549],
            [0.9607843137254902, 0.47058823529411764, 0.058823529411764705],
            [1.0, 0.7843137254901961, 0.27450980392156865],
            [1.0, 0.9019607843137255, 0.8627450980392157],
            [1.0, 1.0, 0.9411764705882353],
            [0.6, 0.9333333333333333, 1.0],
            [0.0, 0.7490196078431373, 1.0],
            [0.0, 0.49411764705882355, 1.0],
            [0.12941176470588237, 0.12941176470588237, 1.0],
            [0.0, 0.0, 0.4392156862745098]]
    return ListedColormap(clist, 'jma_snow_anom_list')

def jma_BlWhRe_linear():
    r'''brown -> orange -> white -> light blue -> blue -> slate blue

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_BlWhRe_linear_256lev``.

    |jma_BlWhRe_linear|

    .. |jma_BlWhRe_linear| image:: ./img/jma_BlWhRe_linear.png
        :width: 600
    '''
    _ncolor = 2
    cdict = {'blue':  [(0/_ncolor, 0/_CMAX, 0/_CMAX),
                   (1/_ncolor, 230/_CMAX, 230/_CMAX),
                   (2/_ncolor, 255/_CMAX, 255/_CMAX)],

              'green': [(0/_ncolor, 40/_CMAX, 40/_CMAX),
                   (1/_ncolor, 255/_CMAX, 255/_CMAX),
                   (2/_ncolor, 65/_CMAX, 65/_CMAX)],

              'red':   [(0/_ncolor,  255/_CMAX, 255/_CMAX),
                  (1/_ncolor, 255/_CMAX, 255/_CMAX),
                  (2/_ncolor, 0/_CMAX, 0/_CMAX)]}
    return LinearSegmentedColormap('jma_BlWhRe_linear', cdict).reversed()

def jma_BlWhRe_list():
    r'''blue -> white -> red

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    The object name is ``jma_BlWhRe_list_11lev``.

    |jma_BlWhRe_list|

    .. |jma_BlWhRe_list| image:: ./img/jma_BlWhRe_list.png
        :width: 600

    See Also
    --------
    jma_BlWhRe_linear
    '''
    clist = [[0.0, 0.2549019607843137, 1.0],
            [1.0, 1.0, 0.9019607843137255],
            [1.0, 0.1568627450980392, 0.0]]
    return ListedColormap(clist, 'jma_BlWhRe_list')


sunshine_256lev = sunshine()
BrWhGr_256lev = BrWhGr()
BlWhRe_256lev = BlWhRe()
precip3_256lev = precip3()
jma_linear_256lev = jma_linear()
jma_list_9lev = jma_list()
grads_default_rainbow_linear_256lev = grads_default_rainbow_linear()
grads_default_rainbow_list_13lev = grads_default_rainbow_list()
grads_paired_256lev = grads_paired()
grads_spectral_256lev = grads_spectral()
grads_rainbow_256lev = grads_rainbow()
grads_b2r_256lev = grads_b2r()
grads_brn2grn_256lev = grads_brn2grn()
grads_y2b_256lev = grads_y2b()
grads_oj2p_256lev = grads_oj2p()
grads_terrain1_256lev = grads_terrain1()
grads_terrain2_256lev = grads_terrain2()
grads_ocean_256lev = grads_ocean()
grads_grayscale_256lev = grads_grayscale()
grads_red_256lev = grads_red()
grads_green_256lev = grads_green()
grads_blue_256lev = grads_blue()
grads_jet_256lev = grads_jet()
grads_dark_256lev = grads_dark()
grads_snow_256lev = grads_snow()
grads_satellite_256lev = grads_satellite()
grads_rain_256lev = grads_rain()
grads_autumn_256lev = grads_autumn()
grads_cool_256lev = grads_cool()
jma_temp_anom_256lev = jma_temp_anom_linear()
jma_temp_anom_11lev = jma_temp_anom_list()
jma_precip_anom_256lev = jma_precip_anom_linear()
jma_precip_anom_11lev = jma_precip_anom_list()
jma_sunlight_anom_256lev = jma_sunlight_anom_linear()
jma_sunlight_anom_11lev = jma_sunlight_anom_list()
jma_snow_anom_256lev = jma_snow_anom_linear()
jma_snow_anom_11lev = jma_snow_anom_list()
jma_BlWhRe_256lev = jma_BlWhRe_linear()
jma_BlWhRe_11lev = jma_BlWhRe_list()

cmap_list = [sunshine_256lev,
            BrWhGr_256lev,
            BlWhRe_256lev,
            precip3_256lev,
            jma_linear_256lev, 
            jma_list_9lev,
            grads_default_rainbow_linear_256lev,
            grads_default_rainbow_list_13lev,
            grads_paired_256lev,
            grads_spectral_256lev,
            grads_rainbow_256lev,
            grads_b2r_256lev,
            grads_brn2grn_256lev,
            grads_y2b_256lev,
            grads_oj2p_256lev,
            grads_terrain1_256lev,
            grads_terrain2_256lev,
            grads_ocean_256lev,
            grads_grayscale_256lev,
            grads_red_256lev,
            grads_green_256lev,
            grads_blue_256lev,
            grads_jet_256lev,
            grads_dark_256lev,
            grads_snow_256lev,
            grads_satellite_256lev,
            grads_rain_256lev,
            grads_autumn_256lev,
            grads_cool_256lev,
            jma_temp_anom_256lev,
            jma_temp_anom_11lev,
            jma_precip_anom_256lev,
            jma_precip_anom_11lev,
            jma_sunlight_anom_256lev,
            jma_sunlight_anom_11lev,
            jma_snow_anom_256lev,
            jma_snow_anom_11lev,
            jma_BlWhRe_256lev,
            jma_BlWhRe_11lev,]


cmap_names = ['sunshine',
            'BrWhGr',
            'BlWhRe',
            'precip3',
            'jma_linear',
            'jma_list',
            'grads_default_rainbow_linear',
            'grads_default_rainbow_list',
            'grads_paired',
            'grads_spectral',
            'grads_rainbow',
            'grads_b2r',
            'grads_brn2grn',
            'grads_y2b',
            'grads_oj2p',
            'grads_terrain1',
            'grads_terrain2',
            'grads_ocean',
            'grads_grayscale',
            'grads_red',
            'grads_green',
            'grads_blue',
            'grads_jet',
            'grads_dark',
            'grads_snow',
            'grads_satellite',
            'grads_rain',
            'grads_autumn',
            'grads_cool',
            'jma_temp_anom_linear',
            'jma_temp_anom_list',
            'jma_precip_anom_linear',
            'jma_precip_anom_list',
            'jma_sunlight_anom_linear',
            'jma_sunlight_anom_list',
            'jma_snow_anom_linear',
            'jma_snow_anom_list',
            'jma_BlWhRe_linear',
            'jma_BlWhRe_list',
            ]


def get_colormap(name):
    r'''カラーマップを得る関数。

    引数の名前は ``get_colormap_list`` で得ることが出来る。

    Parameters
    ----------
    name: `str`
        colormap name

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    See Also
    -----
    get_colormap_list
    '''
    if name in cmap_names:
        return cmap_list[cmap_names.index(name)]
    else:
        print('No such colormap in nakametpy.')
        return sys.exit(1)

def get_colormap_list():
    r'''カラーマップ名のリストを得る関数。

    Returns
    -------
    cmap_names: `List`
    
    '''
    return cmap_names

def _plot_each_colorbar(cmap_name, output='../../docs/img'):
    r'''nakametpy.cmapにあるカラーマップのカラーバーをプロットする関数。

    ドキュメンテーション掲載用。

    nakametpy.cmapのmain()で実行される。
    
    '''
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import os

    fig = plt.figure()
    ax = fig.add_axes([0.05, 0.80, 0.9, 0.06])

    cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', 
                                cmap=get_colormap(cmap_name))

    # ax.set_axis_off()
    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    # # Turn off *all* ticks & spines, not just the ones with colormaps.
    # for i_ax in ax:
    #     i_ax.set_axis_off()

    plt.savefig(os.path.join(output, f'{cmap_name}.png'), bbox_inches='tight', dpi=250)
    plt.close(fig)


MPL_DEFAULT_COLOR_LIST = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def mpl_default_color_cyclic(idx):
    """
    Get matplotlib default color in cyclic

    Parameters
    ----------
    idx: `int`

    Returns
    -------
    color code: `str`
        "#??????"
    """
    return MPL_DEFAULT_COLOR_LIST[idx%len(MPL_DEFAULT_COLOR_LIST)]


if __name__=='__main__':
    for i_cmp_name in get_colormap_list():
        _plot_each_colorbar(i_cmp_name)
    

