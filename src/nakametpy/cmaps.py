from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import sys


CMAX = 255

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
    オブジェクトは*BrWhGr_256lev*という名前でも受け取れる。
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
    '''
    cdict = {'red':   [(0.0,  180/CMAX, 180/CMAX),
                  (1/7, 1., 1.),
                  (2/7, 1., 1.),
                   (3/7,  250/CMAX, 0.),
                  (4/7, 33/CMAX, 33/CMAX),
                   (5/7,  160/CMAX, 160/CMAX),
                   (6/7,  242/CMAX, 242/CMAX),
                   (1, 1, 1)],

         'green': [(0.0,  0, 0),
                   (1/7, 40/CMAX, 40/CMAX),
                  (2/7, 153/CMAX, 153/CMAX),
                   (3/7, 245/CMAX, 65/CMAX),
                   (4/7, 140/CMAX, 140/CMAX),
                   (5/7, 210/CMAX, 210/CMAX),
                   (6/7, 242/CMAX, 242/CMAX),
                   (1,1,1)],

         'blue':  [(0.0,  104/CMAX, 104/CMAX),
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
    オブジェクトは ``jma_list_256lev`` という名前でも受け取れる。
    '''
    clist = [[180/CMAX, 0, 104/CMAX],
            [1., 40/CMAX, 0],
            [1., 153/CMAX, 0],
            [250/CMAX, 245/CMAX, 0],
            [0, 65/CMAX, 1],
            [33/CMAX, 140/CMAX, 1],
            [160/CMAX, 210/CMAX, 1],
            [242/CMAX, 242/CMAX, 1],
            [1, 1, 1]]
            # [242/CMAX, 242/CMAX, 1]]
    return ListedColormap(clist, 'jma_list').reversed()


def grads_default_rainbow_linear():
    r'''GrADSのデフォルトのカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは ``grads_default_rainbow_linear_256lev`` という名前でも受け取れる。
    '''
    cdict = {'red':   [(0.0,  160/CMAX, 160/CMAX),
                    (1/12, 130/CMAX, 130/CMAX),
                    (2/12, 30/CMAX, 30/CMAX),
                    (3/12, 0/CMAX, 0/CMAX),
                    (4/12, 0/CMAX, 0/CMAX),
                    (5/12, 0/CMAX, 0/CMAX),
                    (6/12, 0/CMAX, 0/CMAX),
                    (7/12, 160/CMAX, 160/CMAX),
                    (8/12, 230/CMAX, 230/CMAX),
                    (9/12, 230/CMAX, 230/CMAX),
                    (10/12, 240/CMAX, 240/CMAX),
                    (11/12, 250/CMAX, 250/CMAX),
                    (12/12, 240/CMAX, 240/CMAX)],

            'green': [(0.0,  0, 0),
                    (1/12, 0, 0),
                    (2/12, 60/CMAX, 60/CMAX),
                    (3/12, 160/CMAX, 160/CMAX),
                    (4/12, 200/CMAX, 200/CMAX),
                    (5/12, 210/CMAX, 210/CMAX),
                    (6/12, 220/CMAX, 220/CMAX),
                    (7/12, 230/CMAX, 230/CMAX),
                    (8/12, 220/CMAX, 220/CMAX),
                    (9/12, 175/CMAX, 175/CMAX),
                    (10/12, 130/CMAX, 130/CMAX),
                    (11/12, 60/CMAX, 60/CMAX),
                    (12/12, 0/CMAX, 0/CMAX)],

            'blue':  [(0.0,  200/CMAX, 200/CMAX),
                    (1/12, 220/CMAX, 220/CMAX),
                    (2/12, 255/CMAX, 255/CMAX),
                    (3/12, 255/CMAX, 255/CMAX),
                    (4/12, 200/CMAX, 200/CMAX),
                    (5/12, 210/CMAX, 210/CMAX),
                    (6/12, 0/CMAX, 0/CMAX),
                    (7/12, 50/CMAX, 50/CMAX),
                    (8/12, 50/CMAX, 50/CMAX),
                    (9/12, 45/CMAX, 45/CMAX),
                    (10/12, 40/CMAX, 40/CMAX),
                    (11/12, 60/CMAX, 60/CMAX),
                    (12/12, 130/CMAX, 130/CMAX)]}
    return LinearSegmentedColormap('grads_default_rainbow_linear', cdict)


def grads_default_rainbow_list():
    clist = [[160/CMAX, 0, 200/CMAX],
        [130/CMAX, 0, 220/CMAX],
        [30/CMAX, 60/CMAX, 1],
        [0, 160/CMAX, 1],
        [0, 200/CMAX, 200/CMAX],
        [0, 210/CMAX, 210/CMAX],
        [0, 220/CMAX, 0],
        [160/CMAX, 230/CMAX, 50/CMAX],
        [230/CMAX, 225/CMAX, 50/CMAX],
        [230/CMAX, 170/CMAX, 45/CMAX],
        [240/CMAX, 130/CMAX, 40/CMAX],
        [250/CMAX, 60/CMAX, 60/CMAX],
        [240/CMAX, 0, 130/CMAX]]
    return ListedColormap(clist, 'grads_default_rainbow_list')


def grads_paired():    
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
    cdict = {'blue': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],
    'green': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],
    'red': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_grayscale', cdict)

def grads_red():
    cdict = {'blue': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'green': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'red': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)]}
    return LinearSegmentedColormap('grads_red', cdict)

def grads_green():
    cdict = {'blue': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'green': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],
    'red': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)]}
    return LinearSegmentedColormap('grads_green', cdict)

def grads_blue():
    cdict = {'blue': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],
    'green': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)],
    'red': [(0.0, 1.0, 1.0), (1.0, 0.0, 0.0)]}
    return LinearSegmentedColormap('grads_blue', cdict)

def grads_jet():
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


sunshine_256lev = sunshine()
BrWhGr_256lev = BrWhGr()
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

cmap_list = [sunshine_256lev,
            BrWhGr_256lev,
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
            grads_cool_256lev]


cmap_names = ['sunshine',
            'BrWhGr',
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
            'grads_cool'
            ]


def get_colormap(name):
    if name in cmap_names:
        return cmap_list[cmap_names.index(name)]
    else:
        print('No such colormap in nakametpy.')
        return sys.exit(1)

def get_colormap_list():
    return cmap_names

def _plot_each_colorbar(cmap_name, output='../../img'):
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import os

    fig = plt.figure()
    ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])

    cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', 
                                cmap=get_colormap(cmap_name))

    ax.set_axis_off()
    # # Turn off *all* ticks & spines, not just the ones with colormaps.
    # for i_ax in ax:
    #     i_ax.set_axis_off()

    plt.savefig(os.path.join(output, f'{cmap_name}.png'), bbox_inches='tight', dpi=250)
    plt.close(fig)


if __name__=='__main__':
    for i_cmp_name in get_colormap_list():
        _plot_each_colorbar(i_cmp_name)
    

