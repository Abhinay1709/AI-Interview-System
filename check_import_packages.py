import pkgutil
print('generativeai', any(m.name == 'google.generativeai' for m in pkgutil.iter_modules()))
print('genai', any(m.name == 'google.genai' for m in pkgutil.iter_modules()))
