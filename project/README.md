# О чем эта анкета
Респонденты: носители русского языка, изучавшие (и изучившие на неплохом уровне) английский язык как иностранный.
Цель анкеты: узнать, какой диалект (британский или американский) больше используются носителями сейчас.
В анкете 20 вопросов: 10 на отличающуюся в диалектах лексику и 10 на орфографию.
# Что это за файл backup.txt????
Программа создает файл с таким именем и туда записывает через табуляцию все введенные респондентами ответы.
Просто я на всякий случай оставила вам файл с собранными данными (я сама наобум вводила), на случай, если так будет удобней проверять,
чем так же сто раз наобум вводить.
Просто закомментируйте 252 строчку (make_head()) , и тогда будет использован готовый файл, вместо того чтобы создавать новый.
# Почему такие странные функции для проверки слов? Почему они ищут мелкие куски, а не просто сравнивают введенные данные с нужными словами?
Чтобы не отметать введенное респондентом, если он ошибся в не значимом для опроса месте.
Нам важно лишь понять, какой из двух вариантов лежит в голове носителя, а не то, насколько он грамотен.
Кстати, для опроса используются именно заполняемые формы, а не радио-кнопки с двумя вариантами, чтобы респондент меньше думал над выбором
и просто вписывал то, что первое в голову придет.