set :application, 'defineapalooza'

set :repo_url, 'git@github.com:pobocks/defineapalooza.git'
set :scm, :git
ask :branch, proc { `git rev-parse --abbrev-ref HEAD`.chomp }

set :deploy_to, '/home/defineapalooza/defineapalooza'


# Python stuff

set :pip_requirements, 'requirements.txt'
set :shared_virtualenv, true

set :pty, true

set :linked_files, %w{run.wsgi}
set :linked_dirs, %w{instance}

set :keep_releases, 3


after 'deploy:updating', 'python:create_virtualenv'

namespace :python do

  def virtualenv_path
    File.join(
      fetch(:shared_virtualenv) ? shared_path : release_path, "virtualenv"
    )
  end

  desc "Create a python virtualenv"
  task :create_virtualenv do
    on roles(:all) do |h|
      execute "python3 -m virtualenv #{virtualenv_path}"
      execute "#{virtualenv_path}/bin/pip install -r #{release_path}/#{fetch(:pip_requirements)}"
      if fetch(:shared_virtualenv)
        execute :ln, "-s", virtualenv_path, File.join(release_path, 'virtualenv')
      end
    end
  end
end

namespace :deploy do
  desc 'Restart web server'
  task :restart do
    on roles(:app), in: :sequence, wait: 5 do
      sudo "service httpd restart"
    end
  end

  #after :publishing, 'deploy:restart'

  after :finishing, 'deploy:cleanup'
end
