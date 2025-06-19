import matplotlib.font_manager
fonts = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
print("\n".join(fonts))