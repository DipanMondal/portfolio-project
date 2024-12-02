from django.shortcuts import render, redirect
from .models import PortfolioImage
from portfolio_project import mongo, gemini
from datetime import datetime, date


def public_portfolio(request):
    images = PortfolioImage.objects.all()
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if len(message):
            day = date.today().strftime('%d/%m/%Y')
            time = datetime.now().strftime('%H:%M:%S')
            data = {
                'datetime': day+' '+time,
                'name': name,
                'email': email,
                'message': message
            }
            mongo.insert_feedback(data)

            # update analysis
            analysis = {
                'positive': 0,
                'negative': 0,
                'neutral': 0,
            }
            an = mongo.get_analysis()
            if an:
                analysis['positive'] = an['positive']
                analysis['negative'] = an['negative']
                analysis['neutral'] = an['neutral']
            result = gemini.sentiment(message)
            result = result.lower()
            try:
                analysis[result] = analysis[result] + 1
            except:
                pass
            mongo.modify_analysis(analysis)
        return redirect(public_portfolio)
    return render(request, 'index.html', {'images': images})
