












try:
    
    if __name__ == "__main__":
    
        import PythonResources.Main as go
    
        Apmlication = go.Main()

    else:

        print 'Launching Child Instance...'

except:
    
    import sys
    print sys.exc_info()[0]
    import traceback
    print traceback.format_exc()
    print 'Press Enter to Continue...'
    
    raw_input()
