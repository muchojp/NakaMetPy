from matplotlib.colors import LinearSegmentedColormap

def sunshine():
    r'''
    NCLのcolor table中の `sunshine_9lev` に対応する。
    levelは256である。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----    
    オブジェクトは*sunshine_256lev*という名前でも受け取れる。
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
    r'''
    降水量をプロットする際に利用することを想定したカラーマップ。

    Returns
    -------
    cmap:  `matplotlib.colors.LinearSegmentedColormap`
    
    Notes
    -----
    オブジェクトは `precip3_256lev` という名前でも受け取れる。
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


sunshine_256lev = sunshine()
BrWhGr_256lev = BrWhGr()
precip3_256lev = precip3()
