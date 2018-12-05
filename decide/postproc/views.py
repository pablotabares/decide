from rest_framework.views import APIView
from rest_framework.response import Response
import random


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weight(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weightedRandomSelection(self, options):
        out = []
        n_votes = 0
        for opt in options:
            n_votes += opt["votes"]

        if n_votes == 0:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': False
                })
            return Response(out)

        random_value = random.randint(0, n_votes-1)
        found = False
        for i in range(0, len(options)):
            random_value -= options[i]["votes"]
            if random_value < 0 and not found:
                out.append({
                    **options[i],
                    'postproc': True
                })
                found = True
            else:
                out.append({
                    **options[i],
                    'postproc': False
                })
        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def hondt(self, options, seats):
        out = []
        votes = []
        assignment = []

        for opt in options:
            votes.append({
                'votes': opt['votes'],
            })
            assignment.append({
                'seats': 0
            })

        for i in range(seats):
            max = 0;
            imax = 0;
            for i in range(len(votes)):
                cociente = votes[i]['votes'] / (assignment[i]['seats'] + 1)
                if (cociente > max):
                    max = cociente
                    imax = i
            assignment[imax]['seats'] += 1
        for i in range(len(options)):
            out.append({
                **options[i],
                'postproc': assignment[i]['seats'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def borda(self, options):
        option_positions = {} # {'A': [1,1,2], 'B':[2,2,1]}
        out = {} # {'A':'5', 'B':'4'}
        for opt in options:
            opcion = opt['option']
            posiciones = opt['positions']
            option_positions[opcion] = posiciones

        # We add 1, we have 2 options, I want to do 2+1 - posicion. Fist position 3-1=2 points
        nOptions = len(options) + 1
        for opt_p in option_positions:
            suma = 0
            for p in option_positions.get(opt_p): #We caugth positions [1,1,2]
                suma += nOptions - p #We add points
                
            out[opt_p] = suma 
        return Response(out)
 
    def multiquestion(self, questions):
        out = []

        for question in questions:
            votes = []

            for opt in question['options']:
                votes.append({
                    **opt,
                    'postproc': opt['votes'],
                })

            votes.sort(key=lambda x: -x['postproc'])
            out.append({
                'text': question['text'],
                'options': votes
            })
        return Response(out)

    def genderBalanced(self, options):
        def male_first(male_list, female_list):
            pos = 0
            out = []
            for i in range(0, max(len(male_list), len(female_list))):
                if i < len(male_list):
                    out.append({
                        **male_list[i],
                        'postproc': pos+1,
                    })
                    pos += 1
                if i < len(female_list):
                    out.append({
                        **female_list[i],
                        'postproc': pos+1,
                    })
                    pos += 1
            return out

        def female_first(male_list, female_list):
            pos = 0
            out = []
            for i in range(0, max(len(male_list), len(female_list))):
                if i < len(female_list):
                    out.append({
                        **female_list[i],
                        'postproc': pos+1,
                    })
                    pos += 1
                if i < len(male_list):
                    out.append({
                        **male_list[i],
                        'postproc': pos+1,
                    })
                    pos += 1
            return out

        data_in = options
        data_in.sort(key=lambda x: -x['votes'])
        out = []

        votes = False

        #Checking if there is any vote
        for o in options:
            if o['votes'] != 0:
                votes = True
                break

        # If there is no votes, 'postproc' will be 0 in all the options
        if not votes:
            for opt in options:
                out.append({
                    **opt,
                    'postproc': 0
                })
            return Response(out)


        male_list = [x for x in data_in if x['gender'] == 'MALE']
        female_list = [x for x in data_in if x['gender'] == 'FEMALE']

        pos = 0
        # If there is no male options in the voting
        if not male_list:
            for i in female_list:
                out.append({
                    **i,
                    'postproc': pos+1,
                })
                pos += 1
            return Response(out)

        # If there is no female options in the voting
        if not female_list:
            for i in male_list:
                out.append({
                    **i,
                    'postproc': pos+1,
                })
                pos += 1
            return Response(out)

        # If the most voted option is a man
        if male_list[0]['votes'] > female_list[0]['votes']:
            return  Response(male_first(male_list, female_list))
        elif male_list[0]['votes'] == female_list[0]['votes']:
            sel = random.randint(0, 1)

            # If randomly selected, the first option is a man
            if sel == 0:
                return Response(male_first(male_list, female_list))

            # If randomly selected, the first option is a woman
            else:
                return Response(female_first(male_list, female_list))

        # If the most voted option is a woman
        else:
            return Response(female_first(male_list, female_list))

        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT | BORDA
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t =='WEIGHT':
            return self.weight(opts)
        elif t == 'WEIGHTED-RANDOM':
            return self.weightedRandomSelection(opts)
        elif t == 'HONDT':
            seats = request.data.get('seats', 1)
            return self.hondt(opts, seats)
        elif t == 'BORDA':
            return self.borda(opts)
            seats = request.data.get('seats', 1)
            return self.hondt(opts, seats)
        elif t == 'MULTIPLE':
            questions = request.data.get('questions', [])
            return self.multiquestion(questions)
        elif t == 'GENDER-BALANCED':
            return self.genderBalanced(opts)

        return Response({})
