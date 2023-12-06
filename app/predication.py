def preducation(historical_prices):
    try:
        closedf = historical_prices[['date','close']]
        close_stock = closedf.copy()
        del closedf['date']
        scaler=MinMaxScaler(feature_range=(0,1))
        closedf=scaler.fit_transform(np.array(closedf).reshape(-1,1))

    ## Split data for training and testing (Разделяем данные для обучения и тестирования)
    #Ratio for training and testing data is 65:35 (Соотношение данных для обучения и тестирования составляет 65:35)

        training_size=int(len(closedf)*0.65)
        test_size=len(closedf)-training_size
        train_data,test_data=closedf[0:training_size,:],closedf[training_size:len(closedf),:1]

        time_step = 15
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, y_test = create_dataset(test_data, time_step)

        return X_test, y_train, X_test, y_test

    except Exception as e:
            return f"An error occurred: {str(e)}"


def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)


def randomForestregressor(X_train, y_train, X_test, y_test):
    from sklearn.ensemble import RandomForestRegressor

    regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
    regressor.fit(X_train, y_train)

    # Lets Do the prediction 

    train_predict=regressor.predict(X_train)
    test_predict=regressor.predict(X_test)

    train_predict = train_predict.reshape(-1,1)
    test_predict = test_predict.reshape(-1,1)

    





    


    
